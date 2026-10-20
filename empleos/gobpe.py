"""Lector de gob.pe: anuncios de convocatorias que las instituciones suben a su página.

Dos vías (ambas públicas):
  · búsqueda general (JSON) con términos como «proceso CAS»; trae mucho ruido, por eso se filtra por título y fecha;
  · listado «Convocatoria de trabajo» de cada institución (HTML), limpio y con fecha.
Cada anuncio trae enlace directo al documento (SERVIR no lo da).
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request

from normalizar import sin_tildes

BASE = 'https://www.gob.pe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'setiembre': 9,
         'octubre': 10, 'noviembre': 11, 'diciembre': 12}

# Un anuncio sirve si habla de una convocatoria de personal…
POSITIVO = re.compile(r'convocatoria|proceso cas|\bcas\b|concurso (?:p.blico )?(?:interno )?de m.ritos|proceso de selecci.n|pr.cticas', re.I)
# …y no es otra cosa (resultados, compras, contratos menores, locación, actas…)
NEGATIVO = re.compile(r'resultado|fe de erratas|erratas|acta\b|contrato menor|contratos menores|locaci.n|requerimiento|cotizaci.n|adjudicaci.n|licitaci.n|obra|procompite|'
                      r'adquisici.n|arrendamiento|alquiler|subasta|perito|bono|beca|cuadro multianual|liquidaci.n|bienes|prescripci.n|compra|suministro|servicio de|concurso de ideas|'
                      r'cronograma|lista de|apto|cuestionario|declaraci.n jurada|comunicado', re.I)


class ErrorGobPe(Exception):
    pass


def limpio(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x or ''))).strip()


def fecha_desde_texto(texto):
    """'7 de octubre de 2026' → '2026-10-07' (None si no se entiende)"""
    m = re.search(r'(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(20\d\d)', (texto or '').lower())
    if not m or sin_tildes(m.group(2)) not in MESES:
        return None
    return f'{m.group(3)}-{MESES[sin_tildes(m.group(2))]:02d}-{int(m.group(1)):02d}'


def es_convocatoria(titulo):
    return bool(POSITIVO.search(titulo or '')) and not NEGATIVO.search(titulo or '')


def nombre_institucion(slug):
    return (slug or '').upper().replace('-', ' ')


def _slug_desde_ruta(ruta):
    m = re.match(r'/institucion/([^/]+)/', ruta or '')
    return m.group(1) if m else ''


def _get(url, accept):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept, 'Accept-Language': 'es-PE,es;q=0.9'})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'ignore')


def buscar(termino, paginas=2, pausa=2):
    """Resultados de la búsqueda general de gob.pe: lista de {titulo, url, fecha, institucion, slug}. Solo publicaciones con fecha."""
    salida = []
    for hoja in range(1, paginas + 1):
        u = (BASE + '/busquedas.json?term=' + urllib.parse.quote_plus(termino) + '&contenido%5B%5D=publicaciones&sort_by=recent&sheet=' + str(hoja))
        try:
            datos = json.loads(_get(u, 'application/json'))['data']['attributes']['results']
        except Exception as e:
            raise ErrorGobPe(f'búsqueda «{termino}» falló ({repr(e)[:80]})')
        for r in datos:
            ancla = r.get('url') or ''
            href = re.search(r'href="([^"]+)"', ancla)
            if not href or '/informes-publicaciones/' not in href.group(1):
                continue
            fecha = fecha_desde_texto(r.get('publication'))
            if not fecha:
                continue
            ruta = href.group(1)
            slug = _slug_desde_ruta(ruta)
            salida.append({'titulo': limpio(ancla) or limpio(str(r.get('subject') or '')), 'url': BASE + ruta if ruta.startswith('/') else ruta,
                           'fecha': fecha, 'institucion': nombre_institucion(slug), 'slug': slug, 'fuente': 'gobpe-busqueda'})
        time.sleep(pausa)
    return salida


def listar_institucion(slug, tipo='80-convocatoria-de-trabajo'):
    """Publicaciones del tipo «Convocatoria de trabajo» de una institución, de la más nueva a la más antigua."""
    u = f'{BASE}/institucion/{slug}/informes-publicaciones/tipos/{tipo}'
    try:
        t = _get(u, 'text/html')
    except Exception as e:
        raise ErrorGobPe(f'{slug}: no se pudo leer ({repr(e)[:80]})')
    return leer_tarjetas(t, slug)


def leer_tarjetas(t, slug_defecto=''):
    salida = []
    for li in re.findall(r'<li[^>]*>(.*?)</li>', t, re.S):
        enlace = re.search(r'<a[^>]+class="[^"]*card__mock[^"]*"[^>]*href="(/institucion/[^"]+/informes-publicaciones/\d+-[^"]*)"[^>]*>(.*?)</a>', li, re.S)
        if not enlace:
            continue
        hora = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', li)
        fecha = hora.group(1) if hora else fecha_desde_texto(limpio(li))
        if not fecha:
            continue
        ruta = enlace.group(1)
        slug = _slug_desde_ruta(ruta) or slug_defecto
        salida.append({'titulo': limpio(enlace.group(2)), 'url': BASE + ruta, 'fecha': fecha, 'institucion': nombre_institucion(slug), 'slug': slug,
                       'fuente': 'gobpe-institucion'})
    return salida


def enlaces_pagina(url):
    """Enlaces a publicaciones de una página-colección de gob.pe (para vigilar si aparece uno nuevo): lista de {titulo, url}."""
    try:
        t = _get(url, 'text/html')
    except Exception as e:
        raise ErrorGobPe(f'no se pudo leer {url[-50:]} ({repr(e)[:80]})')
    vistos, salida = set(), []
    for ruta, texto in re.findall(r'<a[^>]+href="(/institucion/[^"]+/informes-publicaciones/\d+-[^"]*)"[^>]*>(.*?)</a>', t, re.S):
        if ruta in vistos:
            continue
        titulo = limpio(texto)
        if len(titulo) < 6:
            continue
        vistos.add(ruta)
        salida.append({'titulo': titulo, 'url': BASE + ruta})
    return salida
