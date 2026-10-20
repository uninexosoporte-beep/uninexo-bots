"""Lector del portal SERVIR · Talento Perú (ofertas laborales y prácticas).

El portal es un formulario JSF/PrimeFaces: se abre la página, se elige la región, se pulsa «Buscar» y se pagina con «Sig.».
No tiene enlace directo por oferta. Se piden pocas páginas y con pausas largas para no cargar el servidor.
"""
import html
import http.cookiejar
import re
import time
import urllib.parse
import urllib.request

from normalizar import sin_tildes

URL_OFERTAS = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/ofertas_laborales.xhtml'
URL_PRACTICAS = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/modalidades_formativas.xhtml'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
CABECERAS = {'Faces-Request': 'partial/ajax', 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


class ErrorServir(Exception):
    pass


def limpio(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x or ''))).strip()


def _clave_etiqueta(etiqueta):
    # el portal parte algunas etiquetas en dos líneas («Número de\n   Convocatoria»): primero se juntan los espacios
    return re.sub(r'[^a-z ]', '', re.sub(r'\s+', ' ', sin_tildes(etiqueta).lower())).strip()


# etiqueta del portal (sin tildes, minúsculas) → campo
ETIQUETAS = {
    'ubicacion': 'ubicacion',
    'numero de convocatoria': 'numero',
    'cantidad de vacantes': 'vacantes',
    'numero de vacante': 'vacantes',
    'remuneracion': 'remuneracion',
    'fecha fin de publicacion': 'fin',
    'cierre de publicacion': 'fin',
    'fecha inicio de publicacion': 'inicio',
    'inicio de publicacion': 'inicio',
    'tipo de modalidad': 'modalidad',
}


def leer_bloques(texto):
    """Ofertas de una respuesta del portal (sirve para ofertas laborales y para prácticas)."""
    ofertas = []
    for bloque in texto.split('cuadro-vacantes')[1:]:
        titulo = re.search(r'titulo-vacante[^>]*>\s*<label>(.*?)</label>', bloque, re.S)
        entidad = re.search(r'nombre-entidad[^>]*>(.*?)</div>', bloque, re.S)
        oferta = {'cargo': limpio(titulo.group(1)) if titulo else '', 'entidad': limpio(entidad.group(1)) if entidad else '',
                  'ubicacion': '', 'numero': '', 'vacantes': '', 'remuneracion': '', 'inicio': '', 'fin': '', 'modalidad': ''}
        for etiqueta, valor in re.findall(r'([^<>]{2,45}?):\s*</(?:span|div)>\s*<(?:span|div)[^>]*detalle-sp[^>]*>(.*?)</(?:span|div)>', bloque, re.S):
            campo = ETIQUETAS.get(_clave_etiqueta(etiqueta))
            if campo and not oferta[campo]:
                oferta[campo] = limpio(valor)
        if oferta['cargo'] or oferta['entidad']:
            ofertas.append(oferta)
    return ofertas


def _nuevo_viewstate(respuesta, actual):
    m = re.search(r'<update id="[^"]*ViewState[^"]*"><!\[CDATA\[([^\]]+)\]\]>', respuesta)
    return m.group(1) if m else actual


def _boton_siguiente(respuesta):
    for m in re.finditer(r'<button id="([^"]+:j_idt\d+)"[^>]*>(?:(?!</button>).)*?ui-button-text ui-c">\s*Sig\.\s*</span>', respuesta, re.S):
        return m.group(1)
    return None


def _leer(url, formulario, region, paginas, pausa):
    """Devuelve (total_puestos, total_paginas, ofertas). `region` = código SERVIR de 2 dígitos o '' para todo el país."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [('User-Agent', UA), ('Accept-Language', 'es-PE,es;q=0.9')]
    try:
        pagina = opener.open(url, timeout=90).read().decode('utf8', 'ignore')
        vs = re.search(r'name="javax.faces.ViewState"[^>]*value="([^"]+)"', pagina).group(1)
        boton = re.search(r'<button id="(' + re.escape(formulario) + r':j_idt\d+)"[^>]*btn-sensitive', pagina).group(1)
    except Exception as e:
        raise ErrorServir(f'no pude abrir la página ({repr(e)[:80]})')

    def enviar(origen, vs):
        datos = {'javax.faces.partial.ajax': 'true', 'javax.faces.source': origen, 'javax.faces.partial.execute': '@all',
                 'javax.faces.partial.render': f'{formulario}:mensaje {formulario}', origen: origen, formulario: formulario,
                 f'{formulario}:cboDep_focus': '', f'{formulario}:cboDep_input': region, 'javax.faces.ViewState': vs}
        req = urllib.request.Request(url, data=urllib.parse.urlencode(datos).encode(), headers=CABECERAS)
        return opener.open(req, timeout=120).read().decode('utf8', 'ignore')

    try:
        r = enviar(boton, vs)
        vs = _nuevo_viewstate(r, vs)
        total = re.search(r'(\d+) puesto\(s\) encontrado', r)
        pags = re.search(r'P.gina\s+\d+\s+de\s+(\d+)', limpio(r))
        total_paginas = int(pags.group(1)) if pags else 1
        ofertas = leer_bloques(r)
        for _ in range(2, min(paginas, total_paginas) + 1):
            time.sleep(pausa)
            siguiente = _boton_siguiente(r)
            if not siguiente:
                break
            r = enviar(siguiente, vs)
            vs = _nuevo_viewstate(r, vs)
            ofertas += leer_bloques(r)
    except ErrorServir:
        raise
    except Exception as e:
        raise ErrorServir(f'falló la consulta ({repr(e)[:80]})')
    return (int(total.group(1)) if total else 0), total_paginas, ofertas


def leer_region(codigo, paginas=3, pausa=5):
    """Ofertas laborales (CAS y otras) de una región, las que cierran más tarde primero."""
    return _leer(URL_OFERTAS, 'frmLstOfertsLabo', codigo, paginas, pausa)


def leer_practicas(paginas=6, pausa=5):
    """Prácticas pre y profesionales de todo el país."""
    return _leer(URL_PRACTICAS, 'frmLstModFormativas', '', paginas, pausa)
