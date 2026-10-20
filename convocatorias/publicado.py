"""Lo que ya está publicado en la pestaña Convocatorias de UniNexo (colección `convocatorias`, lectura pública con filtro de estado): el bot no vuelve a avisar de eso."""
import json
import re
import urllib.request

from clasificar import clave_texto, nombre_institucion
from seleccion import url_canonica

PROYECTO = 'uninexo-produccion'
ESTADOS_VISIBLES = ['active', 'expired', 'broken', 'under_review']  # igual que CONVOCATORIA_ESTADOS_VISIBLES de la app (las reglas rechazan una consulta sin este filtro)


def _tokens(texto):
    return {w for w in clave_texto(texto).split() if len(w) >= 4}


def cargar(proyecto=PROYECTO):
    """Devuelve {'urls': {...}, 'convocatorias': [(titulo, entidad)], 'slugs': {...}}. Si Firestore no responde se lanza la excepción (el bot sigue sin este filtro)."""
    url = f'https://firestore.googleapis.com/v1/projects/{proyecto}/databases/(default)/documents:runQuery'
    cuerpo = {'structuredQuery': {
        'from': [{'collectionId': 'convocatorias'}],
        'where': {'fieldFilter': {'field': {'fieldPath': 'status'}, 'op': 'IN', 'value': {'arrayValue': {'values': [{'stringValue': s} for s in ESTADOS_VISIBLES]}}}},
        'select': {'fields': [{'fieldPath': 'title'}, {'fieldPath': 'organization'}, {'fieldPath': 'officialUrl'}]},
        'limit': 1000}}
    pedido = urllib.request.Request(url, data=json.dumps(cuerpo).encode(), headers={'Content-Type': 'application/json'})
    respuesta = json.load(urllib.request.urlopen(pedido, timeout=60))
    urls, convocatorias, slugs = set(), [], set()
    for fila in respuesta:
        d = fila.get('document')
        if not d:
            continue
        f = d.get('fields', {})
        val = lambda k: (f.get(k) or {}).get('stringValue', '')
        oficial = val('officialUrl')
        if oficial:
            urls.add(url_canonica(oficial))
            m = re.search(r'/institucion/([^/]+)/', oficial)
            if m:
                slugs.add(clave_texto(m.group(1)))
        convocatorias.append((val('title'), val('organization')))
    return {'urls': urls, 'convocatorias': convocatorias, 'slugs': slugs}


def entidad_conocida(c, publicado):
    """¿UniNexo ya tiene una convocatoria de esta entidad? (por su enlace de gob.pe o por el nombre de la entidad)"""
    if clave_texto(c['slug']) in publicado['slugs']:
        return True
    nombre = clave_texto(nombre_institucion(c['slug']))
    return bool(nombre) and any(nombre in clave_texto(entidad) for _, entidad in publicado['convocatorias'])


def ya_publicada(c, publicado):
    """Misma página, o (si es de una entidad ya publicada) una convocatoria con casi el mismo nombre. Para las fichas de entidad: la entidad ya está."""
    if url_canonica(c['enlaceOficial']) in publicado['urls']:
        return True
    if c.get('entidad'):
        return entidad_conocida(c, publicado)
    mios = _tokens(c['name'])
    inst = clave_texto(c['slug'])
    for titulo, entidad in publicado['convocatorias']:
        if inst and inst not in clave_texto(entidad + ' ' + titulo) and clave_texto(c['institucion']) not in clave_texto(entidad):
            continue
        suyos = _tokens(titulo)
        comunes = len(mios & suyos)
        if comunes >= 3 and comunes / max(1, min(len(mios), len(suyos))) >= 0.75:
            return True
    return False
