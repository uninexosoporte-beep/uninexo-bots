"""Textos que el bot de Convocatorias manda a Telegram (HTML). Todos empiezan con 💼 para no confundirlos con los del bot de Empleos ni el de Cursos (📚)."""
from datetime import date

from clasificar import TIPO_ETIQUETA
from seleccion import ORDEN_TIPOS, prioridad
from telegram import esc

DIAS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']


def linea(c, hoy):
    partes = []
    if c.get('entidad'):
        partes.append('entidad nueva en UniNexo')
    if c['fechaLimite']:
        dias = (date.fromisoformat(c['fechaLimite']) - hoy).days
        partes.append(f'cierra {c["fechaLimite"][8:10]}/{c["fechaLimite"][5:7]} ({dias} {"día" if dias == 1 else "días"})')
    else:
        partes.append('sin fecha en la página')
    if c['modalidad']:
        partes.append({'virtual': 'virtual', 'presencial': 'presencial', 'hibrido': 'híbrido'}[c['modalidad']])
    if c['region'] != 'Todo el Perú':
        partes.append(c['region'])
    return f'• <a href="{esc(c["enlaceOficial"])}">{esc(c["name"][:130])}</a>\n   {esc(c["institucion"])} · ' + ' · '.join(esc(p) for p in partes)


def bloques_candidatos(candidatos, hoy):
    """Versión en texto (cuando no hay PDF): una sección por tipo."""
    if not candidatos:
        return []
    bloques = [f'💼 <b>Nuevas convocatorias</b> · {len(candidatos)}\nSon candidatas: confirma fechas y requisitos en cada enlace.']
    por_tipo = {}
    for c in sorted(candidatos, key=prioridad):
        por_tipo.setdefault(c['tipo'], []).append(c)
    for tipo in ORDEN_TIPOS:
        if tipo in por_tipo:
            bloques.append(f'<b>{esc(TIPO_ETIQUETA[tipo])}</b> ({len(por_tipo[tipo])})\n' + '\n'.join(linea(c, hoy) for c in por_tipo[tipo]))
    return bloques


def bloques_paginas(cambios):
    if not cambios:
        return []
    bloques = [f'🔔 <b>Programas vigilados con novedades</b> · {len(cambios)}']
    for c in cambios:
        nuevas = '\n'.join(f'   ＋ {esc(l[:170])}' for l in c['lineas'][:6])
        bloques.append(f'• <a href="{esc(c["url"])}">{esc(c["nombre"])}</a>\n{nuevas}')
    return bloques


def mensaje_resumen(hoy, n_cand, n_entidades, n_paginas, errores, fuentes_ok, con_pdf=False):
    dia = DIAS[hoy.weekday()]
    partes = []
    if n_cand + n_paginas == 0:
        partes.append(f'💼 <b>Convocatorias · {dia} {hoy.strftime("%d/%m")}</b>\nRevisé {fuentes_ok} fuentes y no hay novedades hoy.')
    else:
        partes.append(f'💼 <b>Resumen de convocatorias · {dia} {hoy.strftime("%d/%m")}</b>\nConvocatorias nuevas: {n_cand} (entidades nuevas: {n_entidades}) · Programas con cambios: {n_paginas}'
                      + ('\n📄 Todo el detalle va en el PDF de abajo.' if con_pdf else ''))
    if errores:
        partes.append('⚠️ <b>No pude leer</b>:\n' + '\n'.join(f'   · {esc(e)}' for e in errores[:12]))
    return '\n\n'.join(partes)


def mensaje_inicial(n_enlaces, n_paginas):
    return ('💼 <b>Bot de Convocatorias de UniNexo listo</b>\n'
            f'Hoy aprendí lo que ya existe: {n_enlaces} publicaciones de gob.pe y {n_paginas} programas vigilados. No te envío todo eso para no llenarte el chat.\n\n'
            'Desde ahora, cada día te aviso <b>solo lo nuevo</b>: voluntariados, prácticas (una ficha por entidad que UniNexo todavía no tenga), part-time y programas de primer empleo '
            'de instituciones del Estado, con la fecha límite cuando la página la dice. Te adjunto un informe en PDF y un archivo para importar con el botón «Importar del bot» de la pestaña Convocatorias.')
