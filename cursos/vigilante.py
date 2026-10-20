"""Vigilante de páginas: guarda cómo estaba cada página y avisa de lo que aparece nuevo (enlaces nuevos o líneas nuevas que hablen de becas, cursos o inscripciones)."""
import re
import urllib.request
from html.parser import HTMLParser

import gobpe

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
BLOQUES = {'p', 'div', 'li', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'section', 'article', 'header', 'footer', 'ul', 'ol', 'table'}
IGNORAR = {'script', 'style', 'noscript', 'svg', 'head'}
# Qué líneas nuevas de una página de becas o cursos valen un aviso (el resto de cambios se ignora)
PALABRAS = re.compile(r'beca|scholarship|convocatoria|postul|apply|application|inscripci|matr.cula|plazo|deadline|cronograma|bases|abiert|apertura|curso|diplomado|taller|webinar|'
                      r'programa de|especializaci|pasant|voluntari|internship|2027', re.I)


class _Texto(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lineas, self.actual, self.ignorando = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self.ignorando += 1
        if tag in BLOQUES:
            self._cortar()

    def handle_endtag(self, tag):
        if tag in IGNORAR and self.ignorando:
            self.ignorando -= 1
        if tag in BLOQUES:
            self._cortar()

    def handle_data(self, data):
        if not self.ignorando:
            self.actual.append(data)

    def _cortar(self):
        linea = re.sub(r'\s+', ' ', ''.join(self.actual)).strip()
        if linea:
            self.lineas.append(linea)
        self.actual = []


def lineas_de_html(html_texto):
    """Líneas de texto visibles de una página (sin repetir, ni muy cortas ni larguísimas)."""
    p = _Texto()
    p.feed(html_texto)
    p._cortar()
    vistas, salida = set(), []
    for l in p.lineas:
        if 15 <= len(l) <= 300 and l not in vistas:
            vistas.add(l)
            salida.append(l)
    return salida


def _descargar(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html', 'Accept-Language': 'es-PE,es;q=0.9'})
    return urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'ignore')


def revisar(fuente, alm, hoy_texto):
    """Devuelve {'cambios': [líneas nuevas], 'error': str|None, 'primera': bool}. Guarda el estado nuevo de la página."""
    id_, url = fuente['id'], fuente['url']
    anterior = alm.pagina(id_)
    try:
        if fuente.get('modo') == 'enlaces':
            items = gobpe.enlaces_pagina(url)
            actuales = [f'{i["titulo"]} | {i["url"]}' for i in items]
        else:
            actuales = lineas_de_html(_descargar(url))
    except Exception as e:
        avisar = anterior is None or not anterior['error_avisado']
        alm.marcar_error_pagina(id_, hoy_texto)
        return {'cambios': [], 'error': f'{fuente["nombre"]}: {str(e)[:90]}' if avisar else None, 'primera': False}
    if anterior is None or not anterior['lineas']:
        alm.guardar_pagina(id_, actuales, hoy_texto)
        return {'cambios': [], 'error': None, 'primera': True}
    previas = set(anterior['lineas'])
    nuevas = [l for l in actuales if l not in previas]
    if fuente.get('modo') != 'enlaces':
        nuevas = [l for l in nuevas if PALABRAS.search(l)]
    # se conserva lo anterior + lo actual para que una línea que desaparece y vuelve no cuente como nueva
    alm.guardar_pagina(id_, list(dict.fromkeys(actuales + anterior['lineas']))[:600], hoy_texto)
    return {'cambios': nuevas[:8], 'error': None, 'primera': False}
