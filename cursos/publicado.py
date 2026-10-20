"""Lo que ya está publicado en la sección Cursos de UniNexo (colección `courseOpportunities`, lectura pública): el bot no vuelve a avisar de eso."""
import json
import urllib.parse
import urllib.request

from clasificar import clave_texto
from seleccion import url_canonica

PROYECTO = 'uninexo-produccion'
CAMPOS = ['name', 'institucion', 'enlaceOficial']


def _tokens(texto):
    return {w for w in clave_texto(texto).split() if len(w) >= 4}


def cargar(proyecto=PROYECTO):
    """Devuelve {'urls': {...}, 'cursos': [(nombre, institucion)]}. Si Firestore no responde se lanza la excepción (el bot sigue sin este filtro)."""
    urls, cursos, token = set(), [], None
    for _ in range(20):
        parametros = [('pageSize', '300')] + [('mask.fieldPaths', c) for c in CAMPOS] + ([('pageToken', token)] if token else [])
        url = f'https://firestore.googleapis.com/v1/projects/{proyecto}/databases/(default)/documents/courseOpportunities?' + urllib.parse.urlencode(parametros)
        j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': 'application/json'}), timeout=60))
        for d in j.get('documents', []):
            f = d.get('fields', {})
            val = lambda k: (f.get(k) or {}).get('stringValue', '')
            if val('enlaceOficial'):
                urls.add(url_canonica(val('enlaceOficial')))
            cursos.append((val('name'), val('institucion')))
        token = j.get('nextPageToken')
        if not token:
            break
    return {'urls': urls, 'cursos': cursos}


def ya_publicada(c, publicado):
    """Misma página, o un curso de la misma institución con casi el mismo nombre."""
    if url_canonica(c['enlaceOficial']) in publicado['urls']:
        return True
    mios = _tokens(c['name'])
    inst = clave_texto(c['slug'])
    for nombre, institucion in publicado['cursos']:
        if inst and inst not in clave_texto(institucion + ' ' + nombre) and clave_texto(c['institucion']) not in clave_texto(institucion):
            continue
        suyos = _tokens(nombre)
        comunes = len(mios & suyos)
        if comunes >= 3 and comunes / max(1, min(len(mios), len(suyos))) >= 0.75:
            return True
    return False
