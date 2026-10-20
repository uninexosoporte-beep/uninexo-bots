"""Textos que el bot manda a Telegram (HTML). Cada función devuelve bloques; `telegram.partir` los junta en mensajes de hasta 3800 caracteres."""
import re
from datetime import date

import reglas
from seleccion import fecha_larga
from telegram import esc

DIAS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']


def dias_para(cierre_iso, hoy):
    return (date.fromisoformat(cierre_iso) - hoy).days


def numero_corto(rec):
    n = rec['numero']
    if rec['fuente'] == 'servir-practicas':
        return f'N.º {n}'
    final = re.search(r'-(\d+)$', n)
    num = final.group(1) if final else n
    if rec['tipo'] == 'CAS':
        etiqueta = 'CAS indeterminado' if rec['indeterminado'] else ('CAS suplencia' if 'SUPLENCIA' in n else 'CAS')
        return f'{etiqueta} N.º {num}'
    return f'{rec["tipo"]} N.º {num}'


def linea_oferta(rec, hoy, ampliada=False):
    dias = dias_para(rec['cierre'], hoy)
    cierra = f'{fecha_larga(rec["cierre"])[:5]} ({dias} {"día" if dias == 1 else "días"})'
    sueldo = f'S/ {rec["sueldo"]:,.0f} · ' if rec.get('sueldo') else ''
    marca = '🔄 <b>AMPLIADA</b> · ' if ampliada else ''
    carrera = f' · 🎓 {esc(reglas.etiqueta_carreras(rec["carreras"]))}' if rec.get('carreras') else ''
    return (f'• {marca}<b>{esc(rec["cargo"])}</b> — {esc(rec["institucion"])}\n'
            f'   {sueldo}cierra {cierra} · {esc(numero_corto(rec))} · {esc(rec["distrito"])}{carrera}')


def bloques_plazas(titulo, por_region, hoy, ampliadas=(), cfg=None):
    """por_region: {región: [rec, …]} → bloques de texto, uno por región (las prioritarias primero, con ⭐)."""
    total = sum(len(v) for v in por_region.values())
    bloques = [f'<b>{titulo}</b> · {total} {"plaza" if total == 1 else "plazas"}']
    for region in (reglas.orden_regiones(por_region, cfg) if cfg else sorted(por_region)):
        lineas = [linea_oferta(r, hoy, r['clave_base'] in ampliadas) for r in por_region[region]]
        estrella = '⭐ ' if cfg and reglas.es_prioritaria(region, cfg) else ''
        bloques.append(f'📍 {estrella}<b>{esc(region)}</b> ({len(lineas)})\n' + '\n'.join(lineas))
    return bloques


def bloques_gobpe(items, hoy):
    if not items:
        return []
    bloques = [f'<b>📄 Anuncios de convocatorias en gob.pe</b> · {len(items)}\nNo traen fecha de cierre: revisa las bases en cada enlace.']
    por_institucion = {}
    for it in sorted(items, key=lambda x: x['fecha'], reverse=True):
        por_institucion.setdefault(it['institucion'], []).append(it)
    for institucion, lista in sorted(por_institucion.items(), key=lambda kv: -len(kv[1])):
        lineas = []
        for it in lista[:8]:
            hace = (hoy - date.fromisoformat(it['fecha'])).days
            cuando = 'hoy' if hace <= 0 else ('ayer' if hace == 1 else f'hace {hace} días')
            lineas.append(f'• <a href="{esc(it["url"])}">{esc(it["titulo"][:110])}</a> · {cuando}')
        if len(lista) > 8:
            lineas.append(f'… y {len(lista) - 8} más de {esc(institucion)}')
        bloques.append(f'🏛 <b>{esc(institucion)}</b> ({len(lista)})\n' + '\n'.join(lineas))
    return bloques


def bloques_paginas(cambios):
    """cambios: [{'nombre', 'url', 'lineas': [...]}]"""
    if not cambios:
        return []
    bloques = [f'<b>🔔 Páginas vigiladas con novedades</b> · {len(cambios)}']
    for c in cambios:
        nuevas = '\n'.join(f'   ＋ {esc(l[:170])}' for l in c['lineas'][:6])
        bloques.append(f'• <a href="{esc(c["url"])}">{esc(c["nombre"])}</a>\n{nuevas}')
    return bloques


def mensaje_resumen(hoy, n_servir, n_practicas, n_gobpe, n_paginas, errores, fuentes_ok, con_pdf=False):
    dia = DIAS[hoy.weekday()]
    partes = []
    if n_servir + n_practicas + n_gobpe + n_paginas == 0:
        partes.append(f'✅ <b>Empleos del Estado · {dia} {hoy.strftime("%d/%m")}</b>\nRevisé {fuentes_ok} fuentes y no hay novedades hoy.')
    else:
        partes.append(f'✅ <b>Resumen · {dia} {hoy.strftime("%d/%m")}</b>\nPlazas nuevas: {n_servir} · Prácticas: {n_practicas} · Anuncios gob.pe: {n_gobpe} · Páginas con cambios: {n_paginas}'
                      + ('\n📄 Todo el detalle va en el PDF de abajo.' if con_pdf else ''))
    if errores:
        partes.append('⚠️ <b>No pude leer</b>:\n' + '\n'.join(f'   · {esc(e)}' for e in errores[:12]))
    return '\n\n'.join(partes)


def mensaje_inicial(n_ofertas, n_enlaces, n_paginas):
    return ('🤖 <b>Bot de Empleos de UniNexo listo</b>\n'
            f'Hoy aprendí lo que ya existe: {n_ofertas} plazas, {n_enlaces} anuncios de gob.pe y {n_paginas} páginas vigiladas. '
            'No te envío todo eso para no llenarte el chat.\n\n'
            'Desde ahora, cada día te aviso <b>solo lo nuevo</b>, con la fecha de cierre, y te adjunto un archivo con las plazas listas para publicar.')
