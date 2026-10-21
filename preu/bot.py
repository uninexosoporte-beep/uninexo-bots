"""«Bot Preu» de UniNexo (21/10/2026). Mantiene al día la sección Preu (uninexo.link/preu) SIN publicar nada solo.

  python bot.py               → corrida semanal:
      1. Beca 18: lee la página del PRONABEC; si el cronograma cambió, te lo manda con ✅ Publicar / ❌ Descartar.
      2. Concursos: si en «En proceso» del PRONABEC aparece un concurso nuevo, te avisa (solo aviso).
      3. Enlaces: prueba los enlaces oficiales de Preu y las webs de las universidades; avisa los caídos (2 semanas seguidas).
  python bot.py --aprobaciones → lee tus toques; con ✅ publica el cronograma en Firestore (preu_config/beca18) con la cuenta bot.

Telegram: usa el bot de Convocatorias (.env con TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID; nadie más lee sus respuestas).
Cuenta bot: la del bot de empleos (UNINEXO_CREDENCIALES o config.json → credenciales). Memoria: estado.json.
La primera corrida solo aprende lo que hay (no avisa nada): el cronograma de hoy ya está en la web.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta, timezone

import enlaces
import pronabec
import telegram

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.path.join(AQUI, 'estado.json')
PERU = timezone(timedelta(hours=-5))
TIEMPO_PUBLICADOR = 10 * 60


def hoy_peru():
    return datetime.now(PERU).date()


def cargar_json(ruta, defecto):
    try:
        with open(ruta, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return defecto


def guardar_estado(estado):
    with open(ESTADO + '.tmp', 'w', encoding='utf-8') as fh:
        json.dump(estado, fh, ensure_ascii=False, indent=1)
    os.replace(ESTADO + '.tmp', ESTADO)


def estado_inicial():
    return {'beca18': {'firma': None, 'pendiente': None}, 'concursos': None, 'enlaces': {}, 'offset': 0, 'ultima_semanal': None, 'aviso_error': None}


def descargar(url, timeout=40):
    req = urllib.request.Request(url, headers={'User-Agent': enlaces.AGENTE, 'Accept': 'text/html'})
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception:
            if intento == 2:
                raise
            time.sleep(10)


def fecha_corta(iso):
    a, m, d = iso.split('-')
    return f'{d}/{m}/{a}'


def texto_cronograma(c):
    e = telegram.esc
    lineas = [f'🎓 <b>Beca 18 · {e(c["convocatoria"])}</b>', 'El PRONABEC cambió el cronograma. Esto es lo que leí:', '']
    for f in c['cronograma']:
        cuando = fecha_corta(f['desde']) if f['desde'] == f['hasta'] else f'{fecha_corta(f["desde"])} al {fecha_corta(f["hasta"])}'
        lineas.append(f'• {e(f["que"])}: <b>{cuando}</b>')
    lineas += ['', f'🔗 {pronabec.BECA18_URL}', 'Compáralo con la página. Con ✅ se publica en uninexo.link/preu/becas.']
    return '\n'.join(lineas)


# ---------------------------------------------------------------- corrida semanal

def vigilar_beca18(tg, estado, avisos):
    try:
        datos = pronabec.leer_cronograma(descargar(pronabec.BECA18_URL))
    except Exception as e:
        avisos.append(f'⚠️ No pude abrir la página de Beca 18 ({type(e).__name__}).')
        return
    b = estado['beca18']
    if not datos:
        avisos.append('⚠️ La página de Beca 18 ya no tiene el bloque «CRONOGRAMA»: revísala a mano.')
        return
    f = pronabec.firma(datos)
    if b['firma'] is None:  # primera vez: solo aprende
        b['firma'] = f
        avisos.append('📌 Beca 18: guardé el cronograma actual como punto de partida.')
        return
    if f == b['firma']:
        avisos.append('✅ Beca 18: sin cambios.')
        return
    b['firma'] = f
    if not pronabec.es_publicable(datos):
        tg.enviar(f'⚠️ <b>Beca 18 cambió</b>, pero no pude leer bien las fechas. Revísalo a mano:\n{pronabec.BECA18_URL}')
        avisos.append('⚠️ Beca 18 cambió (sin fechas legibles): avisado.')
        return
    anterior = b.get('pendiente')
    if anterior and anterior.get('estado') == 'pendiente' and anterior.get('mensaje'):
        tg.editar(anterior['mensaje'], texto_cronograma(anterior['datos']) + '\n\n↪️ <b>Reemplazado</b> por una versión más nueva.')
    propuesta = {'convocatoria': datos['convocatoria'], 'cronograma': datos['cronograma'], 'revisado': hoy_peru().isoformat()}
    mid = tg.enviar_con_botones(texto_cronograma(propuesta), [[('✅ Publicar', f'b18pub:{f}'), ('❌ Descartar', f'b18des:{f}')]])
    b['pendiente'] = {'clave': f, 'datos': propuesta, 'estado': 'pendiente', 'mensaje': mid, 'enviado': hoy_peru().isoformat()}
    avisos.append('🆕 Beca 18 cambió: te mandé las fechas para aprobar.')


def vigilar_concursos(tg, estado, avisos):
    try:
        actuales = pronabec.concursos_en_proceso(descargar(pronabec.CONCURSOS_URL))
    except Exception as e:
        avisos.append(f'⚠️ No pude abrir la página de concursos ({type(e).__name__}).')
        return
    if not actuales:
        avisos.append('⚠️ No encontré la sección «En proceso» en la página de concursos: revísala a mano.')
        return
    urls = [c['url'] for c in actuales]
    if estado['concursos'] is None:
        estado['concursos'] = urls
        avisos.append(f'📌 Concursos: guardé los {len(urls)} en proceso como punto de partida.')
        return
    nuevos = [u for u in urls if u not in estado['concursos']]
    estado['concursos'] = sorted(set(estado['concursos']) | set(urls))
    for u in nuevos:
        try:
            nombre = pronabec.titulo_de(descargar(u)) or u
        except Exception:
            nombre = u
        tg.enviar(f'🆕 <b>Nuevo concurso del PRONABEC en proceso</b>\n{telegram.esc(nombre)}\n🔗 {telegram.esc(u)}\n\n'
                  'Míralo: si sirve a escolares o postulantes, se puede sumar a Preu → Becas.')
    avisos.append(f'🆕 Concursos nuevos: {len(nuevos)}.' if nuevos else '✅ Concursos: ninguno nuevo.')


def revisar_enlaces(tg, estado, avisos, cfg):
    lista = cargar_json(os.path.join(AQUI, 'enlaces.json'), [])
    if not lista:
        avisos.append('⚠️ No hay enlaces.json (corre npm run empaquetar:bots en el proyecto).')
        return
    caidos, recuperados, ok = enlaces.revisar(lista, estado['enlaces'], fallos_para_avisar=int(cfg.get('fallos_para_avisar', 2)))
    e = telegram.esc
    if caidos:
        tg.enviar('🔗 <b>Enlaces caídos (2 semanas seguidas)</b>\n' + '\n'.join(f'• {e(n)}: {e(u)} ({e(d)})' for n, u, d in caidos) +
                  '\n\nRevísalos: si cambiaron de dirección, hay que corregirlos en el proyecto.')
    if recuperados:
        tg.enviar('✅ <b>Volvieron a funcionar</b>\n' + '\n'.join(f'• {e(n)}' for n, _, _ in recuperados))
    avisos.append(f'🔗 Enlaces: {ok} de {len(lista)} responden.')


def semanal(tg, estado, cfg):
    avisos = []
    vigilar_beca18(tg, estado, avisos)
    guardar_estado(estado)
    vigilar_concursos(tg, estado, avisos)
    guardar_estado(estado)
    revisar_enlaces(tg, estado, avisos, cfg)
    estado['ultima_semanal'] = hoy_peru().isoformat()
    guardar_estado(estado)
    tg.enviar('🎓 <b>Bot Preu · revisión semanal</b>\n' + '\n'.join(avisos))
    return avisos


# ---------------------------------------------------------------- aprobaciones

def comando_publicador(cfg, archivo):
    """Igual que los otros bots: en GitHub usa el publicador empaquetado (.mjs); en la PC, el proyecto con tsx."""
    paquete = os.environ.get('UNINEXO_PUBLICADOR_DIR')
    if paquete:
        script = os.path.join(paquete, 'publicar-preu-bot.mjs')
        return (['node', script, archivo], os.path.dirname(os.path.abspath(paquete))) if os.path.exists(script) else (None, f'No encuentro {script}.')
    proyecto = cfg.get('proyecto', 'D:/uninexo')
    script = os.path.join(proyecto, 'scripts', 'publicar-preu-bot.ts')
    if not os.path.exists(script):
        return None, f'No encuentro {script}.'
    return (['npx.cmd' if os.name == 'nt' else 'npx', 'tsx', script, archivo], proyecto)


def leer_resumen(salida):
    for linea in reversed((salida or '').splitlines()):
        if linea.startswith('RESUMEN '):
            try:
                return json.loads(linea[len('RESUMEN '):])
            except ValueError:
                return None
    return None


def publicar(cfg, datos, ejecutar=subprocess.run):
    """Devuelve (estado, motivo): publicada | invalida | fallida."""
    cred = telegram.cargar_env(os.environ.get('UNINEXO_CREDENCIALES') or cfg.get('credenciales', 'D:/uninexo-bot/.env'))
    if not cred.get('UNINEXO_BOT_PASSWORD'):
        return 'fallida', 'falta UNINEXO_BOT_PASSWORD en el .env del bot de empleos'
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as fh:
        json.dump(datos, fh, ensure_ascii=False)
        ruta = fh.name
    comando, carpeta = comando_publicador(cfg, ruta)
    try:
        if not comando:
            return 'fallida', carpeta
        entorno = dict(os.environ)
        for k in ('UNINEXO_BOT_PASSWORD', 'UNINEXO_BOT_EMAIL', 'UNINEXO_BOT_APPCHECK_DEBUG'):
            if cred.get(k):
                entorno[k] = cred[k]
        r = ejecutar(comando, cwd=carpeta, env=entorno, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=TIEMPO_PUBLICADOR)
        res = leer_resumen(r.stdout) or {'estado': 'fallida', 'motivo': (r.stderr or 'el publicador no respondió')[-200:]}
        return res.get('estado', 'fallida'), res.get('motivo')
    except (subprocess.TimeoutExpired, OSError) as e:
        return 'fallida', str(e)[:150]
    finally:
        try:
            os.remove(ruta)
        except OSError:
            pass


def aprobaciones(tg, estado, cfg, ejecutar=subprocess.run):
    """Lee toques, vence propuestas viejas y publica lo aprobado. Devuelve un texto corto para el registro."""
    p = estado['beca18'].get('pendiente')
    toques = 0
    for u in tg.actualizaciones(estado.get('offset', 0)):
        estado['offset'] = max(estado.get('offset', 0), u['update_id'] + 1)
        cq = u.get('callback_query')
        if not cq:
            continue
        de = str((cq.get('from') or {}).get('id', ''))
        chat = str(((cq.get('message') or {}).get('chat') or {}).get('id', ''))
        if de != tg.chat_id or chat != tg.chat_id:
            tg.responder_toque(cq['id'], 'Solo el administrador de UniNexo puede aprobar.')
            continue
        accion, _, clave = (cq.get('data') or '').partition(':')
        if not p or p.get('clave') != clave or p.get('estado') != 'pendiente':
            tg.responder_toque(cq['id'], 'Esto ya se revisó.')
            continue
        toques += 1
        if accion == 'b18pub':
            p['estado'] = 'aprobada'
            tg.responder_toque(cq['id'], '✅ Aprobado: lo publico ahora.')
        elif accion == 'b18des':
            p['estado'] = 'descartada'
            tg.responder_toque(cq['id'], '❌ Descartado.')
            tg.editar(p['mensaje'], texto_cronograma(p['datos']) + '\n\n❌ <b>Descartado</b>.')
    # Lo no tocado en 21 días se da por no aprobado
    if p and p.get('estado') == 'pendiente' and p.get('enviado', '9999') < (hoy_peru() - timedelta(days=int(cfg.get('dias_vigencia', 21)))).isoformat():
        p['estado'] = 'vencida'
        tg.editar(p['mensaje'], texto_cronograma(p['datos']) + '\n\n⌛ <b>Venció</b> sin respuesta: no se publicó.')
    guardar_estado(estado)
    if p and p.get('estado') == 'aprobada':
        resultado, motivo = publicar(cfg, p['datos'], ejecutar)
        if resultado == 'publicada':
            p['estado'] = 'publicada'
            tg.editar(p['mensaje'], texto_cronograma(p['datos']) + '\n\n✅ <b>Publicado</b> en uninexo.link/preu/becas (la gente lo ve en hasta 6 horas).')
        elif resultado == 'invalida':
            p['estado'] = 'invalida'
            tg.editar(p['mensaje'], texto_cronograma(p['datos']) + f'\n\n⚠️ <b>No se publicó</b>: {telegram.esc(motivo)}')
        elif estado.get('aviso_error') != hoy_peru().isoformat():
            tg.enviar(f'⚠️ <b>No pude publicar el cronograma de Beca 18</b>: {telegram.esc(motivo)}\nLo vuelvo a intentar en la próxima vuelta.')
            estado['aviso_error'] = hoy_peru().isoformat()
        guardar_estado(estado)
        return f'toques: {toques} · publicación: {resultado}' + (f' ({motivo})' if motivo else '')
    return f'toques: {toques} · nada que publicar'


def main(argv):
    cfg = cargar_json(os.path.join(AQUI, 'config.json'), {})
    env = telegram.cargar_env(os.path.join(AQUI, '.env'))
    tg = telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID'))
    estado = cargar_json(ESTADO, None) or estado_inicial()
    for k, v in estado_inicial().items():
        estado.setdefault(k, v)
    os.makedirs(os.path.join(AQUI, 'logs'), exist_ok=True)
    if '--aprobaciones' in argv:
        resultado = aprobaciones(tg, estado, cfg)
    else:
        resultado = ' | '.join(semanal(tg, estado, cfg))
    linea = f'{datetime.now(PERU):%Y-%m-%d %H:%M} {" ".join(argv) or "semanal"}: {resultado}'
    with open(os.path.join(AQUI, 'logs', 'bot.log'), 'a', encoding='utf-8') as fh:
        fh.write(linea + '\n')
    print(linea)


if __name__ == '__main__':
    main(sys.argv[1:])
