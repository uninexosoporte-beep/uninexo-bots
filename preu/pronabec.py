"""Lectura de las páginas del PRONABEC para el «Bot Preu» (21/10/2026). Funciones puras (sin red): las prueban tests/.

- `leer_cronograma(html)`: convocatoria («Convocatoria 2027») y fechas del bloque CRONOGRAMA … REQUISITOS de la página de Beca 18.
- `concursos_en_proceso(html)`: enlaces de la sección «En proceso» de la página de concursos.
Si el PRONABEC cambia el diseño, estas funciones devuelven vacío y el bot avisa «no pude leer» en vez de publicar algo raro.
"""
import hashlib
import html as html_lib
import json
import re

BECA18_URL = 'https://www.pronabec.gob.pe/beca-18/'
CONCURSOS_URL = 'https://www.pronabec.gob.pe/concursos-becas-creditos/'
MAX_FECHAS = 8  # igual que las reglas de Firestore

_FECHA = r'(\d{1,2})/(\d{1,2})/(20\d\d)'
_ITEM = re.compile(r'([A-ZÁÉÍÓÚÑ][^:()]{2,140}?):\s*(?:del\s+)?' + _FECHA + r'(?:\s*al\s*' + _FECHA + r')?')


def texto_de(html):
    """HTML → texto plano en una sola línea."""
    s = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1>', ' ', html or '')
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html_lib.unescape(s)).strip()


def _iso(d, m, a):
    return f'{int(a):04d}-{int(m):02d}-{int(d):02d}'


def leer_cronograma(html):
    """{'convocatoria', 'cronograma': [{que, desde, hasta}], 'bloque'} o None si no se encuentra el bloque."""
    t = texto_de(html)
    i, j = t.find('CRONOGRAMA'), t.find('REQUISITOS')
    if i < 0 or j <= i:
        return None
    bloque = t[i + len('CRONOGRAMA'):j].replace('Fechas importantes', ' ').strip()
    cronograma = []
    for m in _ITEM.finditer(bloque):
        que = m.group(1).strip(' .-–')
        desde = _iso(*m.group(2, 3, 4))
        hasta = _iso(*m.group(5, 6, 7)) if m.group(5) else desde
        if hasta < desde or not (3 <= len(que) <= 140):
            continue
        cronograma.append({'que': que, 'desde': desde, 'hasta': hasta})
    conv = re.search(r'Convocatoria\s+(20\d\d)', t)
    return {
        'convocatoria': f'Convocatoria {conv.group(1)}' if conv else '',
        'cronograma': cronograma[:MAX_FECHAS],
        'bloque': bloque[:1500],
    }


def firma(datos):
    """Huella corta de lo que importa (si cambia, hay algo nuevo que revisar)."""
    base = json.dumps({'c': datos.get('convocatoria'), 'f': datos.get('cronograma'), 'b': datos.get('bloque') if not datos.get('cronograma') else ''},
                      ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(base.encode('utf-8')).hexdigest()[:12]


def es_publicable(datos):
    """Lo mínimo para ofrecer el botón ✅ (lo demás lo vuelve a revisar el publicador del proyecto)."""
    return bool(datos and re.fullmatch(r'Convocatoria 20\d\d', datos.get('convocatoria') or '') and 1 <= len(datos.get('cronograma') or []) <= MAX_FECHAS)


def concursos_en_proceso(html):
    """[{url}] de la sección «En proceso» (hasta el siguiente título <h2>). Solo páginas del PRONABEC, sin imágenes."""
    s = html or ''
    i = s.find('>En proceso<')
    if i < 0:
        return []
    # La sección termina en el siguiente título (hoy «Nacionales», los concursos externos)
    fin = s.find('<h2', i + len('>En proceso<'))
    seccion = s[i:fin if fin > i else i + 20000]
    vistos, lista = set(), []
    for url in re.findall(r'href="(https://www\.pronabec\.gob\.pe/[^"#?]+)"', seccion):
        url = url.rstrip('/') + '/'
        if '/wp-content/' in url or url in vistos:
            continue
        vistos.add(url)
        lista.append({'url': url})
    return lista


def titulo_de(html):
    """Título de una página del PRONABEC sin la cola «– PRONABEC | …»."""
    m = re.search(r'(?is)<title>(.*?)</title>', html or '')
    titulo = html_lib.unescape(m.group(1)).strip() if m else ''
    return re.split(r'\s+[–-]\s+PRONABEC', titulo)[0].strip()
