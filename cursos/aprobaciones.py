"""Aprobación de cursos con un toque en Telegram (20/10/2026).

1. Cada mañana el bot manda CADA curso candidato como un mensaje con dos botones: ✅ Publicar / ❌ Descartar.
2. Cada 30 minutos (tarea «UniNexo Cursos Aprobaciones», o al empezar la corrida diaria) se leen los toques:
   · solo valen los que vienen del chat del dueño (TELEGRAM_CHAT_ID); los demás se ignoran;
   · ✅ → se publica en Cursos de uninexo.link con el publicador del proyecto (D:\\uninexo\\scripts\\publicar-cursos-bot.ts), que vuelve a
     validar todo y entra con la cuenta bot (solo puede CREAR cursos «sugeridos»);
   · ❌ → se olvida para siempre.
3. El mensaje se actualiza con el resultado (✅ Publicado / ↪️ Ya estaba / ❌ Descartado / ⌛ Venció sin respuesta).
Memoria en aprobaciones.json (cursos enviados y hasta dónde se leyeron los toques). Las credenciales de la cuenta bot NO están aquí:
se leen del .env del bot de empleos (config.json → aprobacion_telegram.credenciales).
"""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import date, timedelta
from urllib.parse import urlparse

import telegram

ARCHIVO = 'aprobaciones.json'
CANDADO = 'aprobaciones.lock'
TIEMPO_MAXIMO = 10 * 60

ETIQUETA_TIPO = {'beca': 'Beca', 'especializacion': 'Especialización', 'diplomado': 'Diplomado', 'curso': 'Curso', 'certificacion': 'Certificación',
                 'taller': 'Taller', 'webinar': 'Webinar / charla', 'voluntariado': 'Voluntariado', 'experiencia_laboral': 'Pasantía',
                 'convocatoria': 'Concurso', 'capacitacion': 'Capacitación'}
ESTADO_TEXTO = {
    'publicada': '✅ <b>Publicado</b> en uninexo.link/cursos (como «sugerido»).',
    'repetida': '↪️ <b>Ya estaba</b> en Cursos: no se repitió.',
    'invalida': '⚠️ <b>No se pudo publicar</b>',
    'descartada': '❌ <b>Descartado</b>. No vuelve a aparecer.',
    'vencida': '⌛ <b>Venció</b> sin respuesta: no se publicó.',
    'aprobada': '⏳ <b>Aprobado</b>: se publica en unos minutos.',
}


def clave_de(enlace):
    """Id corto y estable por enlace (cabe en los 64 bytes que Telegram deja para un botón)."""
    p = urlparse((enlace or '').strip())
    canon = f'{p.netloc.lower().removeprefix("www.")}{p.path.rstrip("/")}'.lower()
    return hashlib.sha1(canon.encode('utf-8')).hexdigest()[:12]


def cargar(aqui):
    try:
        with open(os.path.join(aqui, ARCHIVO), encoding='utf-8') as fh:
            datos = json.load(fh)
            datos.setdefault('offset', 0)
            datos.setdefault('cursos', {})
            return datos
    except (OSError, ValueError):
        return {'offset': 0, 'cursos': {}}


def guardar(aqui, datos):
    ruta = os.path.join(aqui, ARCHIVO)
    with open(ruta + '.tmp', 'w', encoding='utf-8') as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)
    os.replace(ruta + '.tmp', ruta)


def texto_curso(doc):
    """Mensaje de un curso (HTML simple de Telegram)."""
    e = telegram.esc
    partes = [f'📚 <b>{e(doc.get("name", ""))}</b>']
    linea = [x for x in (doc.get('institucion'), ETIQUETA_TIPO.get(doc.get('tipo'), doc.get('tipo')), doc.get('modalidad')) if x]
    partes.append('🏛 ' + e(' · '.join(linea)))
    partes.append('💰 ' + ('Gratis' if doc.get('gratuito') else e(doc.get('costoTexto') or 'Costo por confirmar')))
    if doc.get('fechaLimite'):
        a, m, d = doc['fechaLimite'].split('-')
        partes.append(f'⏳ Cierra el {d}/{m}/{a}')
    if doc.get('area'):
        partes.append('🎓 ' + e(doc['area']))
    partes.append('🔗 ' + e(doc.get('enlaceOficial', '')))
    if doc.get('description'):
        partes.append('\n' + e(doc['description'][:350]))
    return '\n'.join(partes)


def enviar_para_aprobar(tg, docs, hoy, aqui):
    """Manda cada curso nuevo con sus botones. Devuelve cuántos mandó."""
    datos = cargar(aqui)
    enviados = 0
    for doc in docs:
        clave = clave_de(doc.get('enlaceOficial'))
        if clave in datos['cursos']:
            continue  # ya se mandó (aprobado, descartado o pendiente): no se repite
        mid = tg.enviar_con_botones(texto_curso(doc), [[('✅ Publicar', f'pub:{clave}'), ('❌ Descartar', f'des:{clave}')]])
        datos['cursos'][clave] = {'doc': doc, 'estado': 'pendiente', 'mensaje': mid, 'enviado': hoy.isoformat()}
        enviados += 1
        guardar(aqui, datos)  # se guarda de a uno: si Telegram falla a la mitad, no se pierde lo ya enviado
    return enviados


def _cerrar_mensaje(tg, info, estado, motivo=None):
    texto = texto_curso(info['doc']) + '\n\n' + ESTADO_TEXTO.get(estado, estado)
    if motivo and estado in ('invalida', 'fallida'):
        texto += ': ' + telegram.esc(motivo)
    if info.get('mensaje'):
        tg.editar(info['mensaje'], texto)


def leer_toques(tg, datos):
    """Aplica los toques nuevos. Devuelve (aprobados, descartados) en esta vuelta."""
    aprobados = descartados = 0
    for u in tg.actualizaciones(datos['offset']):
        datos['offset'] = max(datos['offset'], u['update_id'] + 1)
        cq = u.get('callback_query')
        if not cq:
            continue
        de = str((cq.get('from') or {}).get('id', ''))
        chat = str(((cq.get('message') or {}).get('chat') or {}).get('id', ''))
        if de != tg.chat_id or chat != tg.chat_id:
            tg.responder_toque(cq['id'], 'Solo el administrador de UniNexo puede aprobar.')
            continue
        accion, _, clave = (cq.get('data') or '').partition(':')
        info = datos['cursos'].get(clave)
        if not info or info['estado'] != 'pendiente':
            tg.responder_toque(cq['id'], 'Este curso ya se revisó.')
            continue
        if accion == 'pub':
            info['estado'] = 'aprobada'
            aprobados += 1
            tg.responder_toque(cq['id'], '✅ Aprobado: se publica en unos minutos.')
        elif accion == 'des':
            info['estado'] = 'descartada'
            descartados += 1
            tg.responder_toque(cq['id'], '❌ Descartado.')
        else:
            continue
        _cerrar_mensaje(tg, info, info['estado'])
    return aprobados, descartados


def vencer(tg, datos, hoy, dias):
    """Lo que nadie tocó en `dias` días se da por no aprobado."""
    limite = (hoy - timedelta(days=dias)).isoformat()
    n = 0
    for info in datos['cursos'].values():
        if info['estado'] == 'pendiente' and info.get('enviado', '9999') < limite:
            info['estado'] = 'vencida'
            _cerrar_mensaje(tg, info, 'vencida')
            n += 1
    return n


def leer_resumen(salida):
    for linea in reversed((salida or '').splitlines()):
        if linea.startswith('RESUMEN '):
            try:
                return json.loads(linea[len('RESUMEN '):])
            except ValueError:
                return None
    return None


def publicar_aprobados(tg, datos, cfg, ejecutar=subprocess.run):
    """Publica lo aprobado con el publicador del proyecto. Devuelve (publicados, error o None)."""
    pendientes = [(k, v) for k, v in datos['cursos'].items() if v['estado'] == 'aprobada']
    if not pendientes:
        return 0, None
    ap = cfg.get('aprobacion_telegram') or {}
    cred = telegram.cargar_env(os.environ.get('UNINEXO_CREDENCIALES') or ap.get('credenciales', 'D:/uninexo-bot/.env'))
    if not cred.get('UNINEXO_BOT_PASSWORD'):
        return 0, 'falta UNINEXO_BOT_PASSWORD en el .env del bot de empleos'
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as fh:
        json.dump([v['doc'] for _, v in pendientes], fh, ensure_ascii=False)
        ruta = fh.name
    comando, carpeta = comando_publicador('publicar-cursos-bot', ap.get('proyecto', 'D:/uninexo'), [ruta])
    if not comando:
        os.remove(ruta)
        return 0, carpeta
    entorno = dict(os.environ)
    for k in ('UNINEXO_BOT_PASSWORD', 'UNINEXO_BOT_EMAIL', 'UNINEXO_BOT_APPCHECK_DEBUG'):
        if cred.get(k):
            entorno[k] = cred[k]
    try:
        r = ejecutar(comando, cwd=carpeta, env=entorno, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=TIEMPO_MAXIMO)
        resumen = leer_resumen(r.stdout)
    except (subprocess.TimeoutExpired, OSError) as e:
        resumen = {'error': str(e)[:150]}
    finally:
        try:
            os.remove(ruta)
        except OSError:
            pass
    if not resumen or not resumen.get('resultados'):
        return 0, (resumen or {}).get('error') or 'el publicador no respondió'  # quedan «aprobadas»: se reintenta en la próxima vuelta
    por_enlace = {x['enlace']: x for x in resumen['resultados']}
    publicados = 0
    for _, info in pendientes:
        res = por_enlace.get(info['doc'].get('enlaceOficial'))
        if not res or res['estado'] in ('nueva', 'fallida'):
            continue  # no se pudo esta vez: sigue «aprobada» y se reintenta
        info['estado'] = res['estado']
        if res['estado'] == 'publicada':
            publicados += 1
        _cerrar_mensaje(tg, info, res['estado'], res.get('motivo'))
    return publicados, resumen.get('error')


def tomar_candado(aqui):
    ruta = os.path.join(aqui, CANDADO)
    if os.path.exists(ruta) and time.time() - os.path.getmtime(ruta) < 20 * 60:
        return False
    with open(ruta, 'w') as fh:
        fh.write(str(os.getpid()))
    return True


def soltar_candado(aqui):
    try:
        os.remove(os.path.join(aqui, CANDADO))
    except OSError:
        pass


def revisar(tg, cfg, hoy, aqui, ejecutar=subprocess.run):
    """Una vuelta completa: leer toques, vencer lo viejo y publicar lo aprobado. Devuelve un texto corto para el log."""
    ap = cfg.get('aprobacion_telegram') or {}
    if not ap.get('activa'):
        return 'aprobación por Telegram apagada'
    if not tomar_candado(aqui):
        return 'otra revisión en marcha'
    try:
        datos = cargar(aqui)
        aprobados, descartados = leer_toques(tg, datos)
        vencidos = vencer(tg, datos, hoy, int(ap.get('dias_vigencia', 14)))
        guardar(aqui, datos)
        publicados, error = publicar_aprobados(tg, datos, cfg, ejecutar)
        guardar(aqui, datos)
        if error and any(v['estado'] == 'aprobada' for v in datos['cursos'].values()):
            # Avisar UNA vez por día si algo aprobado no se puede publicar
            if datos.get('aviso_error') != hoy.isoformat():
                tg.enviar(f'⚠️ <b>No pude publicar los cursos aprobados</b>: {telegram.esc(error)}\nLo vuelvo a intentar cada 30 minutos.')
                datos['aviso_error'] = hoy.isoformat()
                guardar(aqui, datos)
        return f'toques: {aprobados} ✅, {descartados} ❌ · vencidos: {vencidos} · publicados: {publicados}' + (f' · error: {error}' if error else '')
    finally:
        soltar_candado(aqui)


def comando_publicador(nombre, proyecto, archivos):
    """(comando, carpeta) para correr el publicador `nombre` (p. ej. 'publicar-empleos-bot').
    En GitHub Actions UNINEXO_PUBLICADOR_DIR apunta a los publicadores empaquetados (.mjs, solo Node);
    en la PC se usa el proyecto con `npx tsx`. Devuelve (None, motivo) si falta algo."""
    paquete = os.environ.get('UNINEXO_PUBLICADOR_DIR')
    if paquete:
        script = os.path.join(paquete, nombre + '.mjs')
        node = shutil.which('node')
        if not os.path.exists(script) or not node:
            return None, f'No encuentro {script} o Node.'
        return [node, script, *archivos], os.path.dirname(os.path.abspath(paquete))
    script = os.path.join(proyecto, 'scripts', nombre + '.ts')
    if not os.path.exists(script):
        return None, f'No encuentro el publicador en {script}.'
    npx = shutil.which('npx') or shutil.which('npx.cmd')
    if not npx:
        return None, 'No encuentro Node (npx) en esta PC.'
    return [npx, 'tsx', script, *archivos], proyecto
