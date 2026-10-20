"""Lo que ya está publicado en UniNexo (colección `convocatorias_estado`, lectura pública): el bot no vuelve a avisar de eso."""
import json
import re
import urllib.parse
import urllib.request

from normalizar import clave_texto

PROYECTO = 'uninexo-produccion'
CAMPOS = ['cargo', 'institucion', 'distrito', 'fechaCierre', 'descripcion']


def claves_de(numero, cierre, cargo, institucion):
    """Dos formas de reconocer la misma oferta: por número de convocatoria y por entidad."""
    return {('n', clave_texto(numero), cierre, clave_texto(cargo)), ('i', clave_texto(institucion), clave_texto(cargo), cierre)}


def cargar(proyecto=PROYECTO):
    """Conjunto de claves de lo ya publicado. Si Firestore no responde se lanza la excepción (el bot sigue sin este filtro)."""
    claves, token = set(), None
    for _ in range(20):
        parametros = [('pageSize', '300')] + [('mask.fieldPaths', c) for c in CAMPOS] + ([('pageToken', token)] if token else [])
        url = (f'https://firestore.googleapis.com/v1/projects/{proyecto}/databases/(default)/documents/convocatorias_estado?'
               + urllib.parse.urlencode(parametros))
        j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': 'application/json'}), timeout=60))
        for d in j.get('documents', []):
            f = d.get('fields', {})
            val = lambda k: (f.get(k) or {}).get('stringValue', '')
            m = re.search(r'n.mero de convocatoria:\s*(.+?)\.?\s*$', val('descripcion'))
            claves |= claves_de(m.group(1) if m else '', val('fechaCierre'), val('cargo'), val('institucion'))
        token = j.get('nextPageToken')
        if not token:
            break
    return claves


def ya_publicada(rec, claves):
    return bool(claves_de(rec['numero'], rec['cierre'], rec['cargo'], rec['institucion']) & claves)
