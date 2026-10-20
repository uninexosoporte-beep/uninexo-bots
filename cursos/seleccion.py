"""De un resultado de gob.pe al candidato limpio y al documento listo para la cola de revisión de UniNexo (cursos_pendientes)."""
import re
from datetime import date, timedelta
from urllib.parse import unquote, urlsplit

import clasificar
from clasificar import AREA_TODAS, COSTO_POR_CONFIRMAR

AUTOR_BOT = 'Bot de oportunidades'  # nombre público del autor en la cola; no puede llevar «admin», «oficial» ni «uninexo» (reglas de la app)


def url_canonica(url):
    """Misma página aunque cambie el http/https, el www, el final «/» o los parámetros de seguimiento."""
    p = urlsplit(unquote(url or '').strip())
    host = p.netloc.lower().removeprefix('www.')
    return f'{host}{p.path.rstrip("/")}'.lower()


def candidato_desde(item, hoy, leer_pagina=True):
    """item de gob.pe → candidato (o None si no parece una oportunidad de estudio)."""
    titulo = re.sub(r'\s+', ' ', item['titulo']).strip()
    tipo = clasificar.tipo_de(titulo)
    if not tipo or not clasificar.es_oportunidad(titulo, hoy):
        return None
    c = {
        'name': titulo[:150],
        'tipo': tipo,
        'slug': item['slug'],
        'institucion': clasificar.nombre_institucion(item['slug']),
        'enlaceOficial': item['url'],
        'fecha': item['fecha'],
        'fuente': item['fuente'],
        'area': clasificar.area_de(titulo),
        'region': clasificar.region_de(titulo),
        'gratuito': None,
        'costo': None,
        'fechaLimite': None,
        'modalidad': None,
        'descripcion': '',
    }
    if leer_pagina:
        extra = clasificar.leer_pagina(item['url'], hoy)
        if extra.get('soloPersonal'):
            return None  # la página dice que es solo para el personal de una entidad
        c['descripcion'] = extra.get('descripcion', '')
        c['gratuito'] = extra.get('gratuito')
        c['costo'] = extra.get('costo')
        c['fechaLimite'] = extra.get('fechaLimite')
        c['modalidad'] = extra.get('modalidad')
        if c['area'] == AREA_TODAS and c['descripcion']:
            c['area'] = clasificar.area_de(c['descripcion'])
    return c


def clave_titulo(c):
    return f'{clasificar.clave_texto(c["slug"])}|{clasificar.clave_texto(c["name"])}'


def prioridad(c):
    """Orden de importancia en el aviso: becas primero, luego lo que cierra antes."""
    orden = ['beca', 'especializacion', 'diplomado', 'curso', 'certificacion', 'taller', 'webinar', 'voluntariado', 'experiencia_laboral', 'convocatoria']
    return (orden.index(c['tipo']) if c['tipo'] in orden else 99, c['fechaLimite'] or '9999-12-31')


def _fecha_larga(iso):
    a, m, d = iso.split('-')
    return f'{d}/{m}/{a}'


def documento(c, hoy):
    """Lo que se importa a la cola de revisión (`cursos_pendientes`): solo campos que acepta la allowlist de las reglas de la app."""
    gratis = c['gratuito'] is True
    texto = c['descripcion'].strip()
    nota = (f'Detectada automáticamente el {_fecha_larga(hoy.isoformat())} en gob.pe ({c["institucion"]}), publicada el {_fecha_larga(c["fecha"])}. '
            'Revisa las bases en la página oficial antes de aprobarla.')
    doc = {
        'name': c['name'],
        'career': c['area'],
        'region': c['region'],
        'tipo': c['tipo'],
        'enlaceOficial': c['enlaceOficial'],
        'institucion': c['institucion'],
        'gratuito': gratis,
        'description': (texto + ' ' + nota).strip()[:1000],
    }
    if c['area'] != AREA_TODAS:
        doc['area'] = c['area']
    if not gratis:
        doc['costoTexto'] = c['costo'] or COSTO_POR_CONFIRMAR
    if c['fechaLimite']:
        doc['fechaLimite'] = c['fechaLimite']
    if c['modalidad']:
        doc['modalidad'] = c['modalidad']
    return doc
