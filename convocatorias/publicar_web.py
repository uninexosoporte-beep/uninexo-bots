"""Publicación AUTOMÁTICA en la web (20/10/2026): al terminar la corrida, sube las candidatas a Convocatorias de uninexo.link.

No escribe en Firebase por su cuenta: llama al publicador del proyecto (D:\\uninexo\\scripts\\publicar-convocatorias-bot.ts), que valida cada
candidata con el MISMO código del botón «Importar del bot», descarta notas de prensa y repetidas, y las publica como «Detectada automáticamente»
con la cuenta bot de UniNexo (solo puede CREAR; lo dicen las reglas).
Las credenciales de esa cuenta NO se copian aquí: se leen del .env del bot de empleos (config.json → publicacion_automatica.credenciales).
Recuerda qué archivos ya publicó bien (publicados_web.json): si borras una convocatoria en la web, no vuelve a aparecer.
"""
import glob
import json
import os
import shutil
import subprocess
from datetime import timedelta

import telegram

TIEMPO_MAXIMO = 10 * 60  # segundos
MEMORIA = 'publicados_web.json'


def archivos_pendientes(carpeta, hoy, dias, hechos):
    """`candidatas-AAAA-MM-DD*.json` de los últimos `dias` días que aún no se publicaron bien."""
    desde = (hoy - timedelta(days=dias - 1)).isoformat()
    elegidos = []
    for ruta in glob.glob(os.path.join(carpeta, 'candidatas-*.json')):
        nombre = os.path.basename(ruta)
        if nombre[len('candidatas-'):len('candidatas-') + 10] >= desde and nombre not in hechos:
            elegidos.append(ruta)
    return sorted(elegidos)


def leer_resumen(salida):
    for linea in reversed((salida or '').splitlines()):
        if linea.startswith('RESUMEN '):
            try:
                return json.loads(linea[len('RESUMEN '):])
            except ValueError:
                return None
    return None


def _memoria(aqui):
    try:
        with open(os.path.join(aqui, MEMORIA), encoding='utf-8') as fh:
            return set(json.load(fh))
    except (OSError, ValueError):
        return set()


def _guardar_memoria(aqui, hechos):
    with open(os.path.join(aqui, MEMORIA), 'w', encoding='utf-8') as fh:
        json.dump(sorted(hechos), fh, ensure_ascii=False, indent=1)


def publicar(cfg, aqui, hoy, ejecutar=subprocess.run):
    """Devuelve el resumen ({publicadas, …} o {error}) o None si está apagada."""
    pa = cfg.get('publicacion_automatica') or {}
    if not pa.get('activa'):
        return None
    ruta_cred = os.environ.get('UNINEXO_CREDENCIALES') or pa.get('credenciales', 'D:/uninexo-bot/.env')
    cred = telegram.cargar_env(ruta_cred)
    if not cred.get('UNINEXO_BOT_PASSWORD'):
        return {'error': f'Falta UNINEXO_BOT_PASSWORD en {ruta_cred}.'}
    hechos = _memoria(aqui)
    archivos = archivos_pendientes(os.path.join(aqui, 'salida'), hoy, int(pa.get('dias_archivos', 7)), hechos)
    if not archivos:
        return {'publicadas': 0, 'nuevas': 0}
    comando, carpeta = comando_publicador('publicar-convocatorias-bot', pa.get('proyecto', 'D:/uninexo'), archivos)
    if not comando:
        return {'error': carpeta}
    entorno = dict(os.environ)
    for clave in ('UNINEXO_BOT_PASSWORD', 'UNINEXO_BOT_EMAIL', 'UNINEXO_BOT_APPCHECK_DEBUG'):
        if cred.get(clave):
            entorno[clave] = cred[clave]
    try:
        r = ejecutar(comando, cwd=carpeta, env=entorno, capture_output=True, text=True,
                     encoding='utf-8', errors='replace', timeout=TIEMPO_MAXIMO)
    except subprocess.TimeoutExpired:
        return {'error': 'El publicador tardó más de 10 minutos.'}
    except OSError as e:
        return {'error': f'No pude correr el publicador: {e}'}
    resumen = leer_resumen(r.stdout)
    if resumen is None:
        return {'error': f'El publicador no respondió bien (código {r.returncode}).'}
    if not resumen.get('error') and not resumen.get('fallidas'):
        _guardar_memoria(aqui, hechos | {os.path.basename(a) for a in archivos})
    return resumen


def mensaje(resumen):
    """Texto para Telegram (HTML simple)."""
    if resumen is None:
        return None
    if resumen.get('error') and not resumen.get('publicadas'):
        return f'⚠️ <b>No pude publicar en la web</b>: {telegram.esc(resumen["error"])}\nMañana lo intento otra vez.'
    if not resumen.get('publicadas') and not resumen.get('descartadas'):
        return None
    lineas = [f'🌐 <b>Publiqué {resumen.get("publicadas", 0)} convocatorias</b> en uninexo.link (como «Detectada automáticamente»):']
    lineas += [f'   ✅ {telegram.esc(t)}' for t in resumen.get('titulosNuevos', [])[:10]]
    if resumen.get('yaPublicadas'):
        lineas.append(f'   ↪️ {resumen["yaPublicadas"]} ya estaban en la web')
    lineas += [f'   ✖️ {telegram.esc(d)}' for d in resumen.get('descartadas', [])[:5]]
    lineas.append('Si alguna no sirve, bórrala con el menú «⋯» de su tarjeta (no vuelve a aparecer).')
    return '\n'.join(lineas)


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
