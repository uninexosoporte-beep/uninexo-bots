"""Bot de Convocatorias de UniNexo (corre en tu PC una vez al día).

Qué hace: lee gob.pe (campañas de las instituciones nacionales y búsqueda de voluntariados, prácticas, part-time y primer empleo) y algunas páginas de
programas vigiladas; se queda solo con lo nuevo; mira la página de cada convocatoria para ver su fecha límite; y te lo manda a TU Telegram (bot «COMBOCATORIAS
UNINEXO»): un resumen corto, un informe en PDF y un archivo para importar con el botón «Importar del bot» de la pestaña Convocatorias.
Las convocatorias de prácticas NO se avisan una por una: se avisa UNA vez por entidad que UniNexo todavía no tenga. No publica nada por su cuenta.

Uso:
    python bot.py                      corrida normal (la que programa Windows)
    python bot.py --prueba             manda un mensaje y un archivo de prueba a tu Telegram y termina
    python bot.py --simular            hace todo pero NO envía nada ni cambia la memoria (muestra los mensajes en pantalla)
    python bot.py --simular --ver-formato --solo mimp,reniec --sin-busqueda --sin-paginas     prueba rápida de cómo se vería un día normal
    python bot.py --baseline           olvida lo avisado y vuelve a aprender lo que existe hoy, sin avisar
    python bot.py --reglas             muestra tus reglas de tipo e instituciones
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
import time
import traceback
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import almacen  # noqa: E402
import clasificar  # noqa: E402
import gobpe  # noqa: E402
import informe  # noqa: E402
import mensajes  # noqa: E402
import publicado  # noqa: E402
import publicar_web  # noqa: E402
import reglas  # noqa: E402
import seleccion  # noqa: E402
import telegram  # noqa: E402
import vigilante  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LIMITE_SEGUNDOS = 50 * 60  # la tarea de Windows corta a la hora; el bot se frena antes para alcanzar a avisar


def hoy_peru():
    return (datetime.now(timezone.utc) + timedelta(hours=-5)).date()


def log(texto):
    linea = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {texto}'
    print(linea, flush=True)
    try:
        os.makedirs(os.path.join(AQUI, 'logs'), exist_ok=True)
        with open(os.path.join(AQUI, 'logs', f'bot-{datetime.now().strftime("%Y%m")}.log'), 'a', encoding='utf-8') as f:
            f.write(linea + '\n')
    except OSError:
        pass


def leer_json(nombre):
    with open(os.path.join(AQUI, nombre), encoding='utf-8') as f:
        return json.load(f)


def tomar_candado(forzar):
    ruta = os.path.join(AQUI, 'bot.lock')
    if os.path.exists(ruta) and not forzar and time.time() - os.path.getmtime(ruta) < 3 * 3600:
        return False
    with open(ruta, 'w') as f:
        f.write(str(os.getpid()))
    return True


def soltar_candado():
    try:
        os.remove(os.path.join(AQUI, 'bot.lock'))
    except OSError:
        pass


def mostrar_reglas(cfg):
    r = cfg.get('reglas') or {}
    t, i = r.get('tipos') or {}, r.get('instituciones') or {}
    print('REGLAS ACTIVAS (se editan en config.json, sección "reglas")\n')
    print('Tipos:')
    print('  solo estos        :', ', '.join(t.get('solo') or []) or 'todos')
    print('  ignorados         :', ', '.join(t.get('ignorar') or []) or 'ninguno')
    print('Fechas:')
    print('  días de margen    :', r.get('dias_minimos_abierta', 2), '(si la página trae fecha límite)')
    print('Instituciones:')
    print('  siempre incluir   :', ', '.join(i.get('incluir') or []) or 'ninguna')
    print('  ignorar           :', ', '.join(i.get('ignorar') or []) or 'ninguna')
    print('  locales (UGEL, municipios, regiones):', 'sí' if r.get('incluir_locales') else 'no')
    print('Títulos con estas palabras nunca se avisan:', ', '.join(r.get('palabras_excluir') or []) or 'ninguna')
    print('\nTipos válidos:', ', '.join(clasificar.TIPOS))


def es_practica_de_entidad(it):
    """Las convocatorias de prácticas publicadas como documentos (informes-publicaciones) se agrupan por entidad."""
    return it['fuente'] == 'gobpe-publicaciones' and clasificar.tipo_de(it['titulo']) == 'practicas'


def correr(args):
    cfg = leer_json('config.json')
    if args.dias:
        cfg['dias_recientes'] = args.dias
    fuentes = leer_json('fuentes.json')
    env = telegram.cargar_env(os.path.join(AQUI, '.env'))
    hoy = hoy_peru()
    hoy_txt = hoy.isoformat()

    ruta_bd = os.path.join(AQUI, 'estado.sqlite')
    if args.simular:  # trabaja sobre una copia: la memoria real no cambia
        copia = os.path.join(tempfile.gettempdir(), 'uninexo-bot-convocatorias-simulacion.sqlite')
        if os.path.exists(copia):
            os.remove(copia)
        if os.path.exists(ruta_bd) and not args.ver_formato:  # con --ver-formato se parte de una memoria vacía: todo cuenta como nuevo
            shutil.copy(ruta_bd, copia)
        ruta_bd = copia
    alm = almacen.Almacen(ruta_bd)
    if not args.simular and not args.forzar and alm.meta('ultima_corrida') == hoy_txt:
        log('Hoy ya corrió y avisó (máximo una vez al día). Para repetir: python bot.py --forzar')
        alm.cerrar()
        return 0
    inicio = time.time()
    primera = (alm.es_primera_vez() or args.baseline) and not args.ver_formato
    tg = None if args.simular else telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID'))

    errores, por_marcar = [], []
    try:
        pub = publicado.cargar()
        log(f'UniNexo: {len(pub["convocatorias"])} convocatorias ya publicadas en la pestaña (no se avisan)')
    except Exception as e:
        pub = {'urls': set(), 'convocatorias': [], 'slugs': set()}
        log(f'No pude leer lo publicado en UniNexo ({str(e)[:80]}): sigo sin ese filtro')

    # ---------- 1. juntar lo publicado en gob.pe ----------
    items = {}
    camp = next((x for x in fuentes['fuentes'] if x['id'] == 'gobpe-campanas'), {})
    busq = next((x for x in fuentes['fuentes'] if x['id'] == 'gobpe-busqueda'), {})
    extra = (cfg.get('reglas') or {}).get('instituciones', {}).get('incluir') or []
    slugs = list(dict.fromkeys(list(camp.get('slugs', [])) + list(extra)))
    if args.solo:
        pedidos = {x.strip().lower() for x in args.solo.split(',')}
        slugs = [s for s in slugs if s.lower() in pedidos]
    slugs = [s for s in slugs if reglas.institucion_permitida(s, cfg)]
    for i, slug in enumerate(slugs):
        if time.time() - inicio > LIMITE_SEGUNDOS:
            errores.append(f'Se acabó el tiempo (máx. 1 hora). No alcancé a revisar: {", ".join(slugs[i:])}')
            break
        log(f'gob.pe · campañas de {slug} ({i + 1}/{len(slugs)})')
        try:
            for it in gobpe.listar_campanas(slug):
                items.setdefault(seleccion.url_canonica(it['url']), it)
        except Exception as e:
            errores.append(f'gob.pe {slug}: {str(e)[:70]}')
        time.sleep(cfg['pausa_seg'])
    if not args.sin_busqueda and not args.solo:
        for b in busq.get('busquedas', []):
            for contenido in b.get('contenidos', ['campañas']):
                if time.time() - inicio > LIMITE_SEGUNDOS:
                    break
                log(f'gob.pe · búsqueda «{b["termino"]}» en {contenido}')
                try:
                    for it in gobpe.buscar(b['termino'], contenido, b.get('paginas', cfg['busqueda_paginas']), cfg['pausa_seg']):
                        items.setdefault(seleccion.url_canonica(it['url']), it)
                except Exception as e:
                    errores.append(f'gob.pe «{b["termino"]}»: {str(e)[:70]}')

    # ---------- 2. lo nuevo: no visto, reciente, con pinta de convocatoria ----------
    limite_fecha = (hoy - timedelta(days=cfg['dias_recientes'])).isoformat()

    def marcar(it):
        alm.guardar_enlace(seleccion.url_canonica(it['url']), it['fuente'], it['titulo'], it['fecha'], hoy_txt)
        alm.guardar_enlace('t:' + f'{clasificar.clave_texto(it["slug"])}|{clasificar.clave_texto(it["titulo"])}', it['fuente'], it['titulo'], it['fecha'], hoy_txt)

    pendientes = []
    for it in items.values():
        k_titulo = 't:' + f'{clasificar.clave_texto(it["slug"])}|{clasificar.clave_texto(it["titulo"])}'
        if alm.enlace_visto(seleccion.url_canonica(it['url'])) or alm.enlace_visto(k_titulo):
            continue
        if primera or it['fecha'] < limite_fecha or not clasificar.es_oportunidad(it['titulo'], hoy, it['fuente']) or es_practica_de_entidad(it):
            marcar(it)  # lo viejo, lo que no es convocatoria y las prácticas por documento (van por entidad, más abajo) se olvidan en silencio
        else:
            pendientes.append(it)

    candidatos, titulos_hoy, leidas = [], set(), 0
    for it in sorted(pendientes, key=lambda x: x['fecha'], reverse=True):
        leer = leidas < cfg['paginas_a_leer_por_dia'] and time.time() - inicio < LIMITE_SEGUNDOS
        c = seleccion.candidato_desde(it, hoy, leer_pagina=leer)
        if leer:
            leidas += 1
            time.sleep(cfg['pausa_seg'])
        if not c or reglas.evaluar(c, cfg, hoy) or seleccion.clave_titulo(c) in titulos_hoy or publicado.ya_publicada(c, pub):
            marcar(it)
            continue
        titulos_hoy.add(seleccion.clave_titulo(c))
        c['_item'] = it
        candidatos.append(c)

    # ---------- 2b. entidades que publican prácticas y UniNexo todavía no tiene (una ficha por entidad, no una por convocatoria) ----------
    if not primera:
        recientes = {}
        for it in items.values():
            if not es_practica_de_entidad(it) or it['fecha'] < limite_fecha or not clasificar.es_oportunidad(it['titulo'], hoy, it['fuente']):
                continue
            if not reglas.institucion_permitida(it['slug'], cfg):
                continue
            if it['slug'] not in recientes or it['fecha'] > recientes[it['slug']]['fecha']:
                recientes[it['slug']] = it
        for it in sorted(recientes.values(), key=lambda x: x['fecha'], reverse=True):
            c = seleccion.candidato_desde(it, hoy, leer_pagina=False)
            if not c:
                continue
            c = seleccion.a_entidad(c)
            if alm.enlace_visto(seleccion.clave_entidad(c)) or reglas.evaluar(c, cfg, hoy) or publicado.ya_publicada(c, pub):
                continue
            c['_entidad'] = True
            candidatos.append(c)

    candidatos.sort(key=seleccion.prioridad)
    elegidos, sobrantes = candidatos[:cfg['max_por_dia']], candidatos[cfg['max_por_dia']:]
    for c in elegidos:
        if c.get('_entidad'):
            por_marcar.append(lambda c=c: alm.guardar_enlace(seleccion.clave_entidad(c), c['fuente'], c['name'], c['fecha'], hoy_txt))
        else:
            por_marcar.append(lambda it=c['_item']: marcar(it))
    if sobrantes:
        log(f'{len(sobrantes)} candidatas más quedan para mañana (tope de {cfg["max_por_dia"]} por día)')

    # ---------- 3. páginas de programas vigiladas ----------
    cambios_paginas, vigiladas_ok = [], 0
    if not args.sin_paginas and not args.solo:
        for fu in [x for x in fuentes['fuentes'] if x['tipo'] == 'vigilada']:
            if time.time() - inicio > LIMITE_SEGUNDOS:
                errores.append('Se acabó el tiempo (máx. 1 hora) antes de revisar todas las páginas vigiladas')
                break
            log(f'Página vigilada · {fu["nombre"]}')
            res = vigilante.revisar(fu, alm, hoy_txt)
            if res['error']:
                errores.append(res['error'])
            else:
                vigiladas_ok += 1
            if res['cambios']:
                cambios_paginas.append({'nombre': fu['nombre'], 'url': fu['url'], 'lineas': res['cambios']})
            time.sleep(cfg['pausa_seg'])

    # ---------- 4. mensajes ----------
    n_entidades = sum(1 for c in elegidos if c.get('entidad'))
    fuentes_ok = len(slugs) + (0 if (args.sin_busqueda or args.solo) else 1) + vigiladas_ok
    bloques, ruta_pdf, ruta_json = [], None, None
    if primera:
        bloques.append(mensajes.mensaje_inicial(alm.contar_enlaces() // 2, vigiladas_ok))
        if errores:
            bloques.append('⚠️ <b>No pude leer</b>:\n' + '\n'.join(f'   · {telegram.esc(e)}' for e in errores[:12]))
    else:
        hay_novedades = bool(elegidos or cambios_paginas)
        if hay_novedades and cfg.get('formato_aviso', 'pdf') in ('pdf', 'ambos'):
            try:
                html_informe = informe.construir_html(hoy, elegidos, cambios_paginas, errores, cfg)
                carpeta = tempfile.gettempdir() if args.simular else os.path.join(AQUI, 'salida')
                os.makedirs(carpeta, exist_ok=True)
                ruta_pdf = os.path.join(carpeta, f'convocatorias-{hoy_txt}.pdf')
                n = 2
                while os.path.exists(ruta_pdf) and not args.simular:
                    ruta_pdf = os.path.join(carpeta, f'convocatorias-{hoy_txt}-{n}.pdf')
                    n += 1
                informe.html_a_pdf(html_informe, ruta_pdf)
            except informe.ErrorInforme as ex:
                ruta_pdf = None
                errores.append(f'No pude crear el PDF ({str(ex)[:80]}); te mando los mensajes normales')
                log(f'ERROR PDF: {ex}')
        if cfg.get('formato_aviso', 'pdf') in ('mensajes', 'ambos') or (hay_novedades and not ruta_pdf):
            bloques += mensajes.bloques_candidatos(elegidos, hoy)
            bloques += mensajes.bloques_paginas(cambios_paginas)
        if hay_novedades or errores or cfg.get('avisar_si_no_hay_novedades'):
            bloques.append(mensajes.mensaje_resumen(hoy, len(elegidos), n_entidades, len(cambios_paginas), errores, fuentes_ok, con_pdf=bool(ruta_pdf)))

    if elegidos and not args.simular:
        ruta_json = os.path.join(AQUI, 'salida', f'candidatas-{hoy_txt}.json')
        n = 2
        while os.path.exists(ruta_json):
            ruta_json = os.path.join(AQUI, 'salida', f'candidatas-{hoy_txt}-{n}.json')
            n += 1
        os.makedirs(os.path.join(AQUI, 'salida'), exist_ok=True)
        with open(ruta_json, 'w', encoding='utf-8') as fh:
            json.dump([seleccion.documento(c, hoy) for c in elegidos], fh, ensure_ascii=False, indent=2)

    # publicación automática en uninexo.link (también recupera archivos de días anteriores que no se pudieron publicar)
    if not args.simular:
        resumen_web = publicar_web.publicar(cfg, AQUI, hoy)
        texto_web = publicar_web.mensaje(resumen_web)
        if texto_web:
            bloques.append(texto_web)
        if resumen_web is not None:
            log('Web: ' + json.dumps(resumen_web, ensure_ascii=False))

    if args.simular:
        print('\n' + '=' * 70 + '\nSIMULACIÓN: esto es lo que se enviaría a Telegram\n' + '=' * 70)
        for m in telegram.partir(bloques):
            print(m + '\n' + '-' * 70)
        print(f'Convocatorias candidatas para importar: {len(elegidos)}')
        for c in elegidos[:60]:
            print(f'   [{c["tipo"]:<12}] {c["name"][:70]} | {c["institucion"]} | cierre={c["fechaLimite"]} | {"ENTIDAD NUEVA" if c.get("entidad") else c["region"]}')
        if ruta_pdf:
            print(f'PDF de prueba creado en: {ruta_pdf}')
        log(f'Publicaciones vistas: {len(items)} · pendientes de revisar: {len(pendientes)} · páginas leídas: {leidas} · errores: {len(errores)}')
        alm.cerrar()
        return 0

    try:
        tg.enviar_varios(bloques)
        if ruta_pdf:
            tg.enviar_archivo(ruta_pdf, f'💼 Informe de convocatorias · {hoy.strftime("%d/%m/%Y")}')
        if ruta_json:
            tg.enviar_archivo(ruta_json, f'📎 {len(elegidos)} candidatas para importar con el botón «Importar del bot» de la pestaña Convocatorias (tú las revisas antes de publicar).')
    except telegram.ErrorTelegram as e:
        log(f'ERROR de Telegram: {e}. No se marcó nada como avisado: mañana se reintenta.')
        alm.cerrar()
        return 1
    for m in por_marcar:
        m()
    if primera:
        alm.poner_meta('base_inicial', hoy_txt)
    alm.poner_meta('ultima_corrida', hoy_txt)
    log(f'Listo. Convocatorias nuevas: {len(elegidos)}, páginas con cambios: {len(cambios_paginas)}, errores: {len(errores)}')
    alm.cerrar()
    return 0


def main():
    ap = argparse.ArgumentParser(description='Bot de Convocatorias de UniNexo')
    ap.add_argument('--prueba', action='store_true', help='manda un mensaje y un archivo de prueba a tu Telegram')
    ap.add_argument('--simular', action='store_true', help='no envía nada ni cambia la memoria; muestra los mensajes')
    ap.add_argument('--ver-formato', action='store_true', help='con --simular: todo lo reciente cuenta como nuevo (para ver cómo se vería un día normal)')
    ap.add_argument('--baseline', action='store_true', help='vuelve a aprender lo que existe hoy, sin avisar')
    ap.add_argument('--solo', default='', help='solo estas instituciones de gob.pe, separadas por coma (ej. "mimp,reniec")')
    ap.add_argument('--dias', type=int, default=0, help='cuántos días atrás cuentan como «reciente» (solo para pruebas; por defecto sale de config.json)')
    ap.add_argument('--sin-busqueda', action='store_true')
    ap.add_argument('--sin-paginas', action='store_true')
    ap.add_argument('--forzar', action='store_true', help='ignora el candado de otra corrida y el "ya corrió hoy"')
    ap.add_argument('--reglas', action='store_true', help='muestra las reglas activas')
    args = ap.parse_args()

    if args.reglas:
        mostrar_reglas(leer_json('config.json'))
        return 0
    if args.prueba:
        env = telegram.cargar_env(os.path.join(AQUI, '.env'))
        tg = telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID'))
        tg.enviar('🧪 <b>Prueba del bot de Convocatorias de UniNexo</b>\nSi lees esto, el envío a tu Telegram funciona. Enseguida va un archivo de muestra.')
        muestra = {'name': 'Programa de voluntariado de ejemplo (esto es solo una muestra)', 'tipo': 'voluntariado', 'slug': 'reniec', 'institucion': 'RENIEC',
                   'enlaceOficial': 'https://www.gob.pe/institucion/reniec/campa%C3%B1as/0-muestra', 'fecha': hoy_peru().isoformat(), 'fuente': 'gobpe-campañas',
                   'region': 'Todo el Perú', 'fechaLimite': None, 'modalidad': 'presencial', 'descripcion': 'Muestra del formato del archivo.', 'entidad': False}
        ruta = os.path.join(tempfile.gettempdir(), 'muestra-convocatorias-uninexo.json')
        with open(ruta, 'w', encoding='utf-8') as fh:
            json.dump([seleccion.documento(muestra, hoy_peru())], fh, ensure_ascii=False, indent=2)
        tg.enviar_archivo(ruta, '📎 Así llegarán las candidatas para importar (esto es solo una muestra, NO es una convocatoria real).')
        print('Mensaje y archivo de prueba enviados.')
        return 0
    if not tomar_candado(args.forzar):
        log('Ya hay otra corrida en marcha (bot.lock). Saliendo.')
        return 0
    try:
        return correr(args)
    except Exception as e:
        log('FALLÓ: ' + ''.join(traceback.format_exception(e))[-1500:])
        if not args.simular:
            try:
                env = telegram.cargar_env(os.path.join(AQUI, '.env'))
                telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID')).enviar(f'💥 <b>El bot de convocatorias falló hoy</b>\n{telegram.esc(str(e)[:300])}')
            except Exception:
                pass
        return 1
    finally:
        soltar_candado()


if __name__ == '__main__':
    sys.exit(main())
