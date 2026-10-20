"""Textos que el bot de Cursos manda a Telegram (HTML). Todos empiezan con 📚 para no confundirlos con los del bot de Empleos."""
from datetime import date

from clasificar import TIPO_ETIQUETA
from seleccion import prioridad
from telegram import esc

DIAS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
ORDEN_TIPOS = ['beca', 'especializacion', 'diplomado', 'curso', 'certificacion', 'taller', 'webinar', 'voluntariado', 'experiencia_laboral', 'convocatoria']


def linea(c, hoy):
    costo = 'Gratis' if c['gratuito'] is True else (c['costo'] or 'costo por confirmar')
    partes = [costo]
    if c['fechaLimite']:
        dias = (date.fromisoformat(c['fechaLimite']) - hoy).days
        partes.append(f'cierra {c["fechaLimite"][8:10]}/{c["fechaLimite"][5:7]} ({dias} {"día" if dias == 1 else "días"})')
    if c['modalidad']:
        partes.append({'virtual': 'virtual', 'presencial': 'presencial', 'hibrido': 'híbrido'}[c['modalidad']])
    return f'• <a href="{esc(c["enlaceOficial"])}">{esc(c["name"][:130])}</a>\n   {esc(c["institucion"])} · ' + ' · '.join(esc(p) for p in partes)


def bloques_candidatos(candidatos, hoy):
    """Versión en texto (cuando no hay PDF): una sección por tipo."""
    if not candidatos:
        return []
    bloques = [f'📚 <b>Nuevas oportunidades de estudio</b> · {len(candidatos)}\nSon candidatas: confirma costo y fechas en cada enlace.']
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
    bloques = [f'🔔 <b>Páginas de becas y programas con novedades</b> · {len(cambios)}']
    for c in cambios:
        nuevas = '\n'.join(f'   ＋ {esc(l[:170])}' for l in c['lineas'][:6])
        bloques.append(f'• <a href="{esc(c["url"])}">{esc(c["nombre"])}</a>\n{nuevas}')
    return bloques


def mensaje_resumen(hoy, n_cand, n_gratis, n_paginas, errores, fuentes_ok, con_pdf=False):
    dia = DIAS[hoy.weekday()]
    partes = []
    if n_cand + n_paginas == 0:
        partes.append(f'📚 <b>Cursos y Oportunidades · {dia} {hoy.strftime("%d/%m")}</b>\nRevisé {fuentes_ok} fuentes y no hay novedades hoy.')
    else:
        partes.append(f'📚 <b>Resumen de cursos · {dia} {hoy.strftime("%d/%m")}</b>\nOportunidades nuevas: {n_cand} (gratuitas: {n_gratis}) · Páginas con cambios: {n_paginas}'
                      + ('\n📄 Todo el detalle va en el PDF de abajo.' if con_pdf else ''))
    if errores:
        partes.append('⚠️ <b>No pude leer</b>:\n' + '\n'.join(f'   · {esc(e)}' for e in errores[:12]))
    return '\n\n'.join(partes)


def mensaje_inicial(n_enlaces, n_paginas):
    return ('📚 <b>Bot de Cursos y Oportunidades de UniNexo listo</b>\n'
            f'Hoy aprendí lo que ya existe: {n_enlaces} publicaciones de gob.pe y {n_paginas} páginas de becas y programas vigiladas. '
            'No te envío todo eso para no llenarte el chat.\n\n'
            'Desde ahora, cada día te aviso <b>solo lo nuevo</b>: becas, cursos, diplomados, talleres, webinars y voluntariados de instituciones del Estado, '
            'con el costo y la fecha límite cuando la página los dice. Te adjunto un informe en PDF y un archivo para importar a la cola de revisión de Cursos.')
