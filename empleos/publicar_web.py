"""Publicación AUTOMÁTICA en la web (20/10/2026): al terminar la corrida, sube las plazas a Empleos del Estado de uninexo.link.

No escribe en Firebase por su cuenta: llama al publicador del proyecto (D:\\uninexo\\scripts\\publicar-empleos-bot.ts), que valida cada
plaza con el MISMO código del botón «Importar» de la web y entra con la cuenta del bot (solo puede CREAR plazas; lo dicen las reglas).
Se le pasan los archivos `nuevas-*.json` de los últimos días: lo ya publicado se salta solo, así que si un día falla, al siguiente se recupera.
Lo que necesita en el .env: UNINEXO_BOT_PASSWORD (y opcional UNINEXO_BOT_EMAIL). Sin eso, no hace nada y lo dice en el aviso.
"""
import glob
import json
import os
import shutil
import subprocess
from datetime import timedelta

TIEMPO_MAXIMO = 15 * 60  # segundos


def archivos_recientes(carpeta, hoy, dias):
    """`nuevas-AAAA-MM-DD*.json` de los últimos `dias` días (incluido hoy), del más viejo al más nuevo."""
    desde = (hoy - timedelta(days=dias - 1)).isoformat()
    elegidos = []
    for ruta in glob.glob(os.path.join(carpeta, 'nuevas-*.json')):
        fecha = os.path.basename(ruta)[len('nuevas-'):len('nuevas-') + 10]
        if fecha >= desde:
            elegidos.append(ruta)
    return sorted(elegidos)


def leer_resumen(salida):
    """Busca la línea «RESUMEN {json}» que imprime el publicador."""
    for linea in reversed((salida or '').splitlines()):
        if linea.startswith('RESUMEN '):
            try:
                return json.loads(linea[len('RESUMEN '):])
            except ValueError:
                return None
    return None


def publicar(cfg, env, carpeta_salida, hoy, ejecutar=subprocess.run):
    """Devuelve un dict con el resumen ({publicadas, yaPublicadas, …} o {error}) o None si la publicación automática está apagada."""
    pa = cfg.get('publicacion_automatica') or {}
    if not pa.get('activa'):
        return None
    if not env.get('UNINEXO_BOT_PASSWORD'):
        return {'error': 'Falta UNINEXO_BOT_PASSWORD en el .env del bot.'}
    archivos = archivos_recientes(carpeta_salida, hoy, int(pa.get('dias_archivos', 7)))
    if not archivos:
        return {'publicadas': 0, 'nuevas': 0, 'yaPublicadas': 0}
    comando, carpeta = comando_publicador('publicar-empleos-bot', pa.get('proyecto', 'D:/uninexo'), archivos)
    if not comando:
        return {'error': carpeta}
    entorno = dict(os.environ)
    entorno['UNINEXO_BOT_PASSWORD'] = env['UNINEXO_BOT_PASSWORD']
    for clave in ('UNINEXO_BOT_EMAIL', 'UNINEXO_BOT_APPCHECK_DEBUG'):  # el token de App Check del bot (dispositivo de confianza)
        if env.get(clave):
            entorno[clave] = env[clave]
    try:
        r = ejecutar(comando, cwd=carpeta, env=entorno, capture_output=True, text=True,
                     encoding='utf-8', errors='replace', timeout=TIEMPO_MAXIMO)
    except subprocess.TimeoutExpired:
        return {'error': 'El publicador tardó más de 15 minutos.'}
    except OSError as e:
        return {'error': f'No pude correr el publicador: {e}'}
    resumen = leer_resumen(r.stdout)
    if resumen is None:
        return {'error': f'El publicador no respondió bien (código {r.returncode}).'}
    return resumen


def mensaje(resumen):
    """Texto para Telegram (HTML simple)."""
    if resumen is None:
        return None
    if resumen.get('error') and not resumen.get('publicadas'):
        return f'⚠️ <b>No pude publicar en la web</b>: {resumen["error"]}\nLas plazas siguen en el archivo; mañana lo intento otra vez.'
    partes = [f'🌐 <b>Publiqué {resumen.get("publicadas", 0)} plazas</b> en uninexo.link/empleos-estado']
    if resumen.get('yaPublicadas'):
        partes.append(f'{resumen["yaPublicadas"]} ya estaban')
    if resumen.get('conProblemas'):
        partes.append(f'{resumen["conProblemas"]} descartadas (cerradas o con datos raros)')
    if resumen.get('sobrantes'):
        partes.append(f'{resumen["sobrantes"]} quedan para mañana (tope diario)')
    if resumen.get('fallidas'):
        partes.append(f'{resumen["fallidas"]} no se pudieron subir')
    return ' · '.join(partes) + '.'


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
