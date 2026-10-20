"""De un resultado de gob.pe al candidato limpio y al documento que importa la pestaña «Convocatorias» de UniNexo (botón «Importar del bot», solo admin)."""
import re
from urllib.parse import unquote, urlsplit

import clasificar
from clasificar import REGION_TODAS

AUTOR_BOT = 'Bot de oportunidades'  # nombre público del autor; no puede llevar «admin», «oficial» ni «uninexo»
ORDEN_TIPOS = ['voluntariado', 'practicas', 'part_time', 'full_time', 'cas']
MODALIDADES = {'virtual': 'Remoto', 'presencial': 'Presencial', 'hibrido': 'Híbrido'}


def url_canonica(url):
    """Misma página aunque cambie el http/https, el www, el final «/» o los parámetros de seguimiento."""
    p = urlsplit(unquote(url or '').strip())
    host = p.netloc.lower().removeprefix('www.')
    return f'{host}{p.path.rstrip("/")}'.lower()


def candidato_desde(item, hoy, leer_pagina=True):
    """item de gob.pe → candidato (o None si no parece una convocatoria de prácticas, voluntariado o empleo joven)."""
    titulo = re.sub(r'\s+', ' ', item['titulo']).strip()
    tipo = clasificar.tipo_de(titulo)
    if not tipo or not clasificar.es_oportunidad(titulo, hoy, item.get('fuente')):
        return None
    c = {
        'name': titulo[:150],
        'tipo': tipo,
        'slug': item['slug'],
        'institucion': clasificar.nombre_institucion(item['slug']),
        'enlaceOficial': item['url'],
        'fecha': item['fecha'],
        'fuente': item['fuente'],
        'region': clasificar.region_de(titulo),
        'fechaLimite': None,
        'modalidad': None,
        'descripcion': '',
        'entidad': False,
    }
    if leer_pagina:
        extra = clasificar.leer_pagina(item['url'], hoy)
        c['descripcion'] = extra.get('descripcion', '')
        c['fechaLimite'] = extra.get('fechaLimite')
        c['modalidad'] = extra.get('modalidad')
    return c


def a_entidad(c):
    """Una convocatoria de prácticas publicada por una entidad → ficha «Prácticas pre y profesionales en <entidad>».
    Así el bot no inunda de cada convocatoria (INDECOPI saca más de 60 al año): avisa UNA vez por entidad que UniNexo todavía no tenga."""
    muestra = c['name']
    return {**c, 'name': f'Prácticas pre y profesionales en {c["institucion"]}', 'entidad': True, 'fechaLimite': None, 'modalidad': None,
            'descripcion': f'{c["institucion"]} publica en gob.pe sus convocatorias de prácticas. Una reciente: «{muestra}» ({_fecha_larga(c["fecha"])}).'}


def clave_titulo(c):
    return f'{clasificar.clave_texto(c["slug"])}|{clasificar.clave_texto(c["name"])}'


def clave_entidad(c):
    return f'e:{clasificar.clave_texto(c["slug"])}'


def prioridad(c):
    """Orden de importancia en el aviso: voluntariados y prácticas primero, y lo que cierra antes."""
    return (ORDEN_TIPOS.index(c['tipo']) if c['tipo'] in ORDEN_TIPOS else 99, c['fechaLimite'] or '9999-12-31')


def _fecha_larga(iso):
    a, m, d = iso.split('-')
    return f'{d}/{m}/{a}'


def documento(c, hoy):
    """Lo que se importa a `convocatorias`: solo campos que acepta la regla `isValidConvocatoriaData` (probado en test-emulador/convocatoriasIniciales.test.ts)."""
    texto = c['descripcion'].strip()
    nota = (f'Detectada automáticamente el {_fecha_larga(hoy.isoformat())} en gob.pe ({c["institucion"]}), publicada el {_fecha_larga(c["fecha"])}. '
            'Revisa las bases en la página oficial antes de publicarla.')
    doc = {
        'title': c['name'],
        'organization': c['institucion'][:120],
        'category': c['tipo'],
        'sector': 'Sector Público',
        'location': (c['region'] or REGION_TODAS)[:100],
        'description': (texto + ' ' + nota).strip()[:1000],
        'officialUrl': c['enlaceOficial'],
    }
    if c['fechaLimite']:
        doc['deadline'] = c['fechaLimite']
    if c['modalidad']:
        doc['modalidad'] = MODALIDADES[c['modalidad']]
    return doc
