"""Bot de Empleos de UniNexo (corre en tu PC una vez al día).

Qué hace: lee SERVIR (ofertas y prácticas de las 25 regiones), gob.pe (anuncios de convocatorias) y algunas páginas vigiladas;
se queda solo con lo nuevo y abierto; y te lo manda a TU Telegram, junto con un archivo de plazas listas para publicar en UniNexo.
No publica nada por su cuenta.

Uso:
    python bot.py                      corrida normal (la que programa Windows)
    python bot.py --prueba             manda un mensaje de prueba a tu Telegram y termina
    python bot.py --simular            hace todo pero NO envía nada ni cambia la memoria (muestra los mensajes en pantalla)
    python bot.py --simular --solo Arequipa,Cusco --sin-gobpe --sin-paginas --sin-practicas     prueba rápida
    python bot.py --simular --ver-formato --solo Arequipa --sin-gobpe --sin-paginas --sin-practicas     cómo se vería un día normal
    python bot.py --baseline           olvida lo avisado y vuelve a aprender lo que existe hoy, sin avisar
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
import gobpe  # noqa: E402
import informe  # noqa: E402
import mensajes  # noqa: E402
import publicado  # noqa: E402
import publicar_web  # noqa: E402
import reglas  # noqa: E402
import seleccion  # noqa: E402
import servir  # noqa: E402
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


def con_reintentos(fn, intentos=2, espera=60):
    for i in range(intentos):
        try:
            return fn()
        except Exception as e:
            if i == intentos - 1:
                raise
            log(f'   falló ({str(e)[:80]}); reintento en {espera} s')
            time.sleep(espera)


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
    """Resumen de tus reglas (las que se editan en config.json → "reglas") y de las carreras que el bot sabe reconocer."""
    r = cfg.get('reglas') or {}
    reg, car, cargos = r.get('regiones') or {}, r.get('carreras') or {}, r.get('cargos') or {}
    f = cfg['filtros']
    print('REGLAS ACTIVAS (se editan en config.json, sección "reglas")\n')
    print('Regiones:')
    print('  solo estas        :', ', '.join(reg.get('solo') or []) or 'todas')
    print('  ignoradas         :', ', '.join(reg.get('ignorar') or []) or 'ninguna')
    print('  prioritarias ⭐   :', ', '.join(reg.get('prioritarias') or []) or 'ninguna')
    print('  tope propio       :', reg.get('tope_propio') or f'ninguno (tope general: {f["max_por_region"]} por región)')
    print('Carreras:')
    print('  solo estas        :', ', '.join(car.get('solo') or []) or 'todas (solo etiqueta cada plaza con su carrera)')
    print('  ignoradas         :', ', '.join(car.get('ignorar') or []) or 'ninguna')
    print('  sin carrera clara :', 'pasan' if car.get('incluir_sin_carrera', True) else 'se descartan')
    print('Cargos:')
    print('  excluir palabras  :', ', '.join(cargos.get('excluir_palabras') or []) or 'ninguna')
    print('  siempre incluir   :', ', '.join(cargos.get('incluir_palabras') or []) or 'ninguna')
    print('\nCarreras que el bot reconoce (usa estos nombres en "solo" / "ignorar"):')
    for nombre in reglas.CARRERAS:
        print('  -', nombre)


def correr(args):
    cfg = leer_json('config.json')
    fuentes = leer_json('fuentes.json')
    env = telegram.cargar_env(os.path.join(AQUI, '.env'))
    hoy = hoy_peru()
    hoy_txt = hoy.isoformat()

    ruta_bd = os.path.join(AQUI, 'estado.sqlite')
    if args.simular:  # trabaja sobre una copia: la memoria real no cambia
        copia = os.path.join(tempfile.gettempdir(), 'uninexo-bot-simulacion.sqlite')
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
        claves_pub = publicado.cargar()
        log(f'UniNexo: {len(claves_pub) // 2} convocatorias ya publicadas (no se avisan)')
    except Exception as e:
        claves_pub = set()
        log(f'No pude leer lo publicado en UniNexo ({str(e)[:80]}): sigo sin ese filtro')

    f = cfg['filtros']
    cs = cfg['servir']
    nuevas_servir, nuevas_practicas = {}, {}
    ampliadas = set()
    leidas = {'ofertas': 0, 'practicas': 0, 'gobpe': 0}

    def procesar(recs, destino):
        """Aplica filtros, memoria y elección a las ofertas de UNA región; llena `destino` y la lista de marcas pendientes."""
        recs = seleccion.sin_repetidas(recs)
        candidatas = []
        for r in recs:
            if seleccion.motivo_descarte(r, cfg, hoy):
                continue
            guardada = alm.cierre_guardado(r['clave_base'])
            if primera:
                alm.guardar_oferta(r['clave_base'], r['fuente'], r['region'], r['cargo'], r['cierre'], hoy_txt, avisada=0)
            elif guardada is None:
                if publicado.ya_publicada(r, claves_pub):
                    alm.guardar_oferta(r['clave_base'], r['fuente'], r['region'], r['cargo'], r['cierre'], hoy_txt, avisada=0)
                else:
                    candidatas.append(r)
            elif r['cierre'] > guardada:  # la entidad amplió el plazo
                ampliadas.add(r['clave_base'])
                candidatas.append(r)
        if primera or not candidatas:
            return
        elegidas, _ = seleccion.elegir(candidatas, cfg)
        for r in elegidas:
            destino.setdefault(r['region'], []).append(r)
            por_marcar.append(lambda r=r: alm.guardar_oferta(r['clave_base'], r['fuente'], r['region'], r['cargo'], r['cierre'], hoy_txt))

    # ---------- SERVIR · ofertas laborales ----------
    if not args.sin_servir:
        regiones = cfg['regiones']
        if args.solo:
            pedidas = {x.strip().lower() for x in args.solo.split(',')}
            regiones = {k: v for k, v in regiones.items() if k.lower() in pedidas}
        # tus reglas de región: las ignoradas ni se leen, y las prioritarias se leen primero (si se acaba el tiempo, ellas ya están)
        regiones = {k: v for k, v in regiones.items() if reglas.region_permitida(k, cfg)}
        regiones = dict(sorted(regiones.items(), key=lambda kv: not reglas.es_prioritaria(kv[0], cfg)))
        for i, (nombre, codigo) in enumerate(regiones.items()):
            if time.time() - inicio > LIMITE_SEGUNDOS:  # tope de 1 hora por día: se corta y se avisa lo que faltó
                faltaron = ', '.join(list(regiones)[i:])
                errores.append(f'Se acabó el tiempo (máx. 1 hora). No alcancé a revisar: {faltaron}')
                log(f'   TIEMPO AGOTADO: faltaron {faltaron}')
                break
            log(f'SERVIR · {nombre} ({i + 1}/{len(regiones)})')
            try:
                total, paginas, crudas = con_reintentos(lambda: servir.leer_region(codigo, cs['paginas_por_region'], cs['pausa_entre_paginas_seg']))
            except Exception as e:
                errores.append(f'SERVIR {nombre}: {str(e)[:80]}')
                log(f'   ERROR {e}')
                crudas = []
            leidas['ofertas'] += len(crudas)
            recs = [r for r in (seleccion.convertir(o, 'servir-ofertas', nombre) for o in crudas) if r]
            procesar(recs, nuevas_servir)
            if i < len(regiones) - 1:
                time.sleep(cs['pausa_entre_regiones_seg'])

    # ---------- SERVIR · prácticas ----------
    if not args.sin_practicas and not args.solo:
        log('SERVIR · prácticas (todo el país)')
        try:
            total, paginas, crudas = con_reintentos(lambda: servir.leer_practicas(cs['paginas_practicas'], cs['pausa_entre_paginas_seg']))
            leidas['practicas'] = len(crudas)
            por_region = {}
            for o in crudas:
                r = seleccion.convertir(o, 'servir-practicas')
                if r:
                    por_region.setdefault(r['region'], []).append(r)
            for recs in por_region.values():
                procesar(recs, nuevas_practicas)
        except Exception as e:
            errores.append(f'SERVIR prácticas: {str(e)[:80]}')
            log(f'   ERROR {e}')

    # ---------- gob.pe ----------
    nuevos_gobpe = []
    if not args.sin_gobpe and not args.solo:
        g = cfg['gobpe']
        vistos_ahora = {}
        busqueda = next((x for x in fuentes['fuentes'] if x['id'] == 'gobpe-busqueda'), None)
        instituciones = next((x for x in fuentes['fuentes'] if x['id'] == 'gobpe-instituciones'), None)
        for termino in (busqueda or {}).get('terminos', []):
            log(f'gob.pe · búsqueda «{termino}»')
            try:
                for it in gobpe.buscar(termino, g['paginas_busqueda'], g['pausa_seg']):
                    if gobpe.es_convocatoria(it['titulo']) and not reglas.evaluar_texto(it['titulo'], reglas.carreras_de(it['titulo']), cfg):
                        vistos_ahora[it['url']] = it
            except Exception as e:
                errores.append(f'gob.pe «{termino}»: {str(e)[:70]}')
        for slug in (instituciones or {}).get('slugs', []):
            log(f'gob.pe · {slug}')
            try:
                for it in gobpe.listar_institucion(slug, g['tipo_convocatoria']):
                    if not gobpe.NEGATIVO.search(it['titulo']) and not reglas.evaluar_texto(it['titulo'], reglas.carreras_de(it['titulo']), cfg):
                        vistos_ahora.setdefault(it['url'], it)
            except Exception as e:
                errores.append(f'gob.pe {slug}: {str(e)[:70]}')
            time.sleep(g['pausa_seg'])
        leidas['gobpe'] = len(vistos_ahora)
        limite_fecha = (hoy - timedelta(days=g['dias_recientes'])).isoformat()
        for url, it in vistos_ahora.items():
            if alm.enlace_visto(url):
                continue
            if primera or it['fecha'] < limite_fecha:
                alm.guardar_enlace(url, it['fuente'], it['titulo'], it['fecha'], hoy_txt)
            else:
                nuevos_gobpe.append(it)
                por_marcar.append(lambda it=it: alm.guardar_enlace(it['url'], it['fuente'], it['titulo'], it['fecha'], hoy_txt))

    # ---------- páginas vigiladas ----------
    cambios_paginas, vigiladas_ok, primeras = [], 0, 0
    if not args.sin_paginas and not args.solo:
        for fu in [x for x in fuentes['fuentes'] if x['tipo'] == 'vigilada']:
            log(f'Página vigilada · {fu["nombre"]}')
            res = vigilante.revisar(fu, alm, hoy_txt)
            if res['error']:
                errores.append(res['error'])
            else:
                vigiladas_ok += 1
            primeras += 1 if res['primera'] else 0
            if res['cambios']:
                cambios_paginas.append({'nombre': fu['nombre'], 'url': fu['url'], 'lineas': res['cambios']})

    # ---------- mensajes ----------
    n_servir = sum(len(v) for v in nuevas_servir.values())
    n_pract = sum(len(v) for v in nuevas_practicas.values())
    fuentes_ok = (0 if args.sin_servir else 1) + (0 if (args.sin_practicas or args.solo) else 1) + (0 if (args.sin_gobpe or args.solo) else 2) + vigiladas_ok
    bloques, ruta_pdf = [], None
    if primera:
        bloques.append(mensajes.mensaje_inicial(alm.contar_ofertas(), alm.contar_enlaces(), vigiladas_ok))
        if errores:
            bloques.append('⚠️ <b>No pude leer</b>:\n' + '\n'.join(f'   · {telegram.esc(e)}' for e in errores[:12]))
    else:
        hay_novedades = bool(nuevas_servir or nuevas_practicas or nuevos_gobpe or cambios_paginas)
        formato = cfg.get('formato_aviso', 'mensajes')  # 'pdf' (informe en PDF), 'mensajes' (texto en Telegram) o 'ambos'
        if hay_novedades and formato in ('pdf', 'ambos'):
            try:
                html_informe = informe.construir_html(hoy, nuevas_servir, nuevas_practicas, nuevos_gobpe, cambios_paginas, errores, cfg, ampliadas)
                carpeta_pdf = tempfile.gettempdir() if args.simular else os.path.join(AQUI, 'salida')
                os.makedirs(carpeta_pdf, exist_ok=True)
                ruta_pdf = os.path.join(carpeta_pdf, f'empleos-{hoy_txt}.pdf')
                n = 2
                while os.path.exists(ruta_pdf) and not args.simular:
                    ruta_pdf = os.path.join(carpeta_pdf, f'empleos-{hoy_txt}-{n}.pdf')
                    n += 1
                informe.html_a_pdf(html_informe, ruta_pdf)
            except informe.ErrorInforme as ex:
                ruta_pdf = None
                errores.append(f'No pude crear el PDF ({str(ex)[:80]}); te mando los mensajes normales')
                log(f'ERROR PDF: {ex}')
        if formato in ('mensajes', 'ambos') or (hay_novedades and not ruta_pdf):
            if nuevas_servir:
                bloques += mensajes.bloques_plazas('🆕 Nuevas plazas en el Estado', nuevas_servir, hoy, ampliadas, cfg)
            if nuevas_practicas:
                bloques += mensajes.bloques_plazas('🎓 Nuevas prácticas', nuevas_practicas, hoy, ampliadas, cfg)
            bloques += mensajes.bloques_gobpe(nuevos_gobpe[:25], hoy)
            if len(nuevos_gobpe) > 25:
                bloques.append(f'… y {len(nuevos_gobpe) - 25} anuncios más en gob.pe.')
            bloques += mensajes.bloques_paginas(cambios_paginas)
        if hay_novedades or errores or cfg.get('avisar_si_no_hay_novedades'):
            bloques.append(mensajes.mensaje_resumen(hoy, n_servir, n_pract, len(nuevos_gobpe), len(cambios_paginas), errores, fuentes_ok, con_pdf=bool(ruta_pdf)))

    # archivo con las plazas en el formato de UniNexo
    recs_archivo = [r for v in list(nuevas_servir.values()) + list(nuevas_practicas.values()) for r in v]
    ruta_archivo = None
    if recs_archivo:
        docs = [seleccion.documento(r, i) for r, i in zip(recs_archivo, seleccion.ids_para(recs_archivo, hoy))]
        nombre = f'nuevas-{hoy_txt}.json'
        if not args.simular:
            ruta_archivo = os.path.join(AQUI, 'salida', nombre)
            n = 2
            while os.path.exists(ruta_archivo):
                ruta_archivo = os.path.join(AQUI, 'salida', f'nuevas-{hoy_txt}-{n}.json')
                n += 1
            os.makedirs(os.path.join(AQUI, 'salida'), exist_ok=True)
            with open(ruta_archivo, 'w', encoding='utf-8') as fh:
                json.dump(docs, fh, ensure_ascii=False, indent=2)

    # publicación automática en uninexo.link (también recupera lo que quedó pendiente de días anteriores)
    if not args.simular:
        resumen_web = publicar_web.publicar(cfg, env, os.path.join(AQUI, 'salida'), hoy)
        texto_web = publicar_web.mensaje(resumen_web)
        if texto_web:
            bloques.append(texto_web)
            log('Web: ' + json.dumps(resumen_web, ensure_ascii=False))

    if args.simular:
        print('\n' + '=' * 70 + '\nSIMULACIÓN: esto es lo que se enviaría a Telegram\n' + '=' * 70)
        for m in telegram.partir(bloques):
            print(m + '\n' + '-' * 70)
        print(f'Archivo de plazas listas para publicar: {len(recs_archivo)} plazas')
        if ruta_pdf:
            print(f'PDF de prueba creado en: {ruta_pdf}')
        log(f'Leído: {leidas} · errores: {len(errores)}')
        alm.cerrar()
        return 0

    try:
        tg.enviar_varios(bloques)
        if ruta_pdf:
            tg.enviar_archivo(ruta_pdf, f'📄 Informe de empleos del Estado · {hoy.strftime("%d/%m/%Y")}')
        if ruta_archivo:
            tg.enviar_archivo(ruta_archivo, f'📎 {len(recs_archivo)} plazas en el formato de UniNexo (para el botón «Importar» o para pasárselas a Claude).')
    except telegram.ErrorTelegram as e:
        log(f'ERROR de Telegram: {e}. No se marcó nada como avisado: mañana se reintenta.')
        alm.cerrar()
        return 1
    for marcar in por_marcar:
        marcar()
    if primera:
        alm.poner_meta('base_inicial', hoy_txt)
    alm.poner_meta('ultima_corrida', hoy_txt)
    log(f'Listo. Plazas nuevas: {n_servir}, prácticas: {n_pract}, anuncios gob.pe: {len(nuevos_gobpe)}, páginas con cambios: {len(cambios_paginas)}, errores: {len(errores)}')
    alm.cerrar()
    return 0


def main():
    ap = argparse.ArgumentParser(description='Bot de Empleos de UniNexo')
    ap.add_argument('--prueba', action='store_true', help='manda un mensaje de prueba a tu Telegram')
    ap.add_argument('--simular', action='store_true', help='no envía nada ni cambia la memoria; muestra los mensajes')
    ap.add_argument('--baseline', action='store_true', help='vuelve a aprender lo que existe hoy, sin avisar')
    ap.add_argument('--ver-formato', action='store_true', help='con --simular: muestra cómo se vería un día normal (todo lo que pase los filtros cuenta como nuevo)')
    ap.add_argument('--solo', default='', help='solo estas regiones de SERVIR, separadas por coma (ej. "Arequipa,Cusco")')
    ap.add_argument('--sin-servir', action='store_true')
    ap.add_argument('--sin-practicas', action='store_true')
    ap.add_argument('--sin-gobpe', action='store_true')
    ap.add_argument('--sin-paginas', action='store_true')
    ap.add_argument('--forzar', action='store_true', help='ignora el candado de otra corrida y el "ya corrió hoy"')
    ap.add_argument('--reglas', action='store_true', help='muestra las reglas de región y carrera activas y las carreras disponibles')
    args = ap.parse_args()

    if args.prueba:
        env = telegram.cargar_env(os.path.join(AQUI, '.env'))
        tg = telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID'))
        tg.enviar('🧪 <b>Prueba del bot de Empleos de UniNexo</b>\nSi lees esto, el envío a tu Telegram funciona. Enseguida va un archivo de muestra.')
        muestra = seleccion.convertir({'cargo': 'ESPECIALISTA EN CONTABILIDAD', 'entidad': 'MUNICIPALIDAD DISTRITAL DE SAN PABLO', 'ubicacion': 'CUSCO - SAN PABLO',
                                       'numero': 'D.LEG 1057 - DETERMINADO (NECESIDAD TRANSITORIA)-8', 'vacantes': '1', 'remuneracion': 'S/. 3,500.00', 'fin': '31/12/2026',
                                       'inicio': '', 'modalidad': ''}, 'servir-ofertas', 'Cusco')
        ruta = os.path.join(tempfile.gettempdir(), 'muestra-plazas-uninexo.json')
        with open(ruta, 'w', encoding='utf-8') as fh:
            json.dump([seleccion.documento(muestra, 'ce-cusco-muestra-01')], fh, ensure_ascii=False, indent=2)
        tg.enviar_archivo(ruta, '📎 Así llegarán las plazas listas para publicar (esto es solo una muestra, NO es una oferta real).')
        print('Mensaje y archivo de prueba enviados.')
        return 0
    if args.reglas:
        mostrar_reglas(leer_json('config.json'))
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
                telegram.Telegram(env.get('TELEGRAM_BOT_TOKEN'), env.get('TELEGRAM_CHAT_ID')).enviar(f'💥 <b>El bot de empleos falló hoy</b>\n{telegram.esc(str(e)[:300])}')
            except Exception:
                pass
        return 1
    finally:
        soltar_candado()


if __name__ == '__main__':
    sys.exit(main())
