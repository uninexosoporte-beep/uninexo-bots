"""Lector de gob.pe para convocatorias de prácticas, voluntariado y empleo joven.

Tres vías públicas:
  · búsqueda general (JSON) en «campañas», «noticias» y «publicaciones» con términos como «voluntariado» o «convocatoria de prácticas»;
  · lista de «campañas» de cada institución nacional (HTML) con su fecha de publicación;
  · lista de enlaces de una página-colección (para vigilarla).
Cada resultado trae enlace directo a la página de la institución.
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request

BASE = 'https://www.gob.pe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'setiembre': 9,
         'octubre': 10, 'noviembre': 11, 'diciembre': 12}
SECCIONES = {'campañas': 'campa', 'noticias': 'noticias', 'publicaciones': 'informes-publicaciones'}


class ErrorGobPe(Exception):
    pass


def limpio(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x or ''))).strip()


def sin_tildes(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def fecha_desde_texto(texto):
    """'7 de octubre de 2026' → '2026-10-07' (None si no se entiende)"""
    m = re.search(r'(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(20\d\d)', (texto or '').lower())
    if not m or sin_tildes(m.group(2)) not in MESES:
        return None
    return f'{m.group(3)}-{MESES[sin_tildes(m.group(2))]:02d}-{int(m.group(1)):02d}'


def slug_de_ruta(ruta):
    m = re.match(r'/institucion/([^/]+)/', urllib.parse.unquote(ruta or ''))
    return m.group(1) if m else ''


def descargar(url, accept='text/html', limite=1_500_000):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept, 'Accept-Language': 'es-PE,es;q=0.9'})
    return urllib.request.urlopen(req, timeout=60).read(limite).decode('utf-8', 'ignore')


def buscar(termino, contenido, paginas=1, pausa=2):
    """Búsqueda general. `contenido`: 'campañas', 'noticias' o 'publicaciones'. Devuelve [{titulo, url, fecha, slug, fuente}] (solo con fecha)."""
    salida = []
    for hoja in range(1, paginas + 1):
        u = (BASE + '/busquedas.json?term=' + urllib.parse.quote_plus(termino) + '&contenido%5B%5D=' + urllib.parse.quote(contenido) + '&sort_by=recent&sheet=' + str(hoja))
        try:
            datos = json.loads(descargar(u, 'application/json'))['data']['attributes']['results']
        except Exception as e:
            raise ErrorGobPe(f'búsqueda «{termino}» en {contenido} falló ({repr(e)[:80]})')
        for r in datos:
            if not isinstance(r, dict):  # gob.pe a veces manda un resultado vacío (null) en medio de la lista
                continue
            ancla = r.get('url') or ''
            href = re.search(r'href="([^"]+)"', ancla)
            fecha = fecha_desde_texto(r.get('publication'))
            if not href or not fecha or SECCIONES[contenido] not in urllib.parse.unquote(href.group(1)):
                continue
            ruta = href.group(1)
            salida.append({'titulo': limpio(ancla) or limpio(str(r.get('subject') or '')), 'url': BASE + ruta if ruta.startswith('/') else ruta,
                           'fecha': fecha, 'slug': slug_de_ruta(ruta), 'fuente': f'gobpe-{contenido}'})
        time.sleep(pausa)
    return salida


def listar_campanas(slug):
    """Campañas (voluntariados, programas de empleo joven, pasantías) publicadas por una institución, con su fecha de publicación."""
    u = f'{BASE}/institucion/{slug}/' + urllib.parse.quote('campañas')
    try:
        t = descargar(u)
    except Exception as e:
        raise ErrorGobPe(f'{slug}: no se pudo leer ({repr(e)[:80]})')
    return leer_tarjetas_campanas(t, slug)


def leer_tarjetas_campanas(t, slug):
    salida, vistos = [], set()
    for li in re.findall(r'<li[^>]*>(.*?)</li>', t, re.S):
        a = re.search(r'<a[^>]+href="(/institucion/[^"]+/campa[^"]+/\d+-[^"]*)"[^>]*>(.*?)</a>', li, re.S)
        if not a:
            continue
        ruta = a.group(1)
        hora = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', li)
        fecha = hora.group(1) if hora else fecha_desde_texto(limpio(li))
        titulo = limpio(a.group(2))
        if not fecha or len(titulo) < 5 or ruta in vistos:
            continue
        vistos.add(ruta)
        salida.append({'titulo': titulo, 'url': BASE + ruta, 'fecha': fecha, 'slug': slug_de_ruta(ruta) or slug, 'fuente': 'gobpe-campañas'})
    return salida


def enlaces_pagina(url):
    """Enlaces a publicaciones de una página-colección de gob.pe (para vigilar si aparece uno nuevo): lista de {titulo, url}."""
    try:
        t = descargar(url)
    except Exception as e:
        raise ErrorGobPe(f'no se pudo leer {url[-50:]} ({repr(e)[:80]})')
    vistos, salida = set(), []
    for ruta, texto in re.findall(r'<a[^>]+href="(/institucion/[^"]+/(?:informes-publicaciones|campa[^"/]*)/\d+-[^"]*)"[^>]*>(.*?)</a>', t, re.S):
        if ruta in vistos:
            continue
        titulo = limpio(texto)
        if len(titulo) < 6:
            continue
        vistos.add(ruta)
        salida.append({'titulo': titulo, 'url': BASE + ruta})
    return salida
