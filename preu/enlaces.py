"""Revisor semanal de enlaces oficiales del «Bot Preu» (21/10/2026).

Un enlace se da por CAÍDO solo si falla 2 semanas seguidas (las webs del Estado a veces no responden o bloquean un rato los
servidores de GitHub). Se avisa una vez cuando cae y otra cuando vuelve. La lista sale del proyecto (enlaces.json).
"""
import urllib.error
import urllib.request

AGENTE = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 UniNexoBot/1.0 (+https://uninexo.link)'


def probar(url, timeout=25):
    """(ok, detalle). ok = la página responde con un código menor a 400."""
    req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'text/html,*/*'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            r.read(2048)
            return r.status < 400, str(r.status)
    except urllib.error.HTTPError as e:
        return e.code < 400, str(e.code)
    except Exception as e:  # sin conexión, certificado, tiempo agotado…
        return False, type(e).__name__


def revisar(lista, memoria, probar_fn=probar, fallos_para_avisar=2):
    """Actualiza `memoria` ({url: {'fallos': n, 'avisado': bool}}) y devuelve (caidos_nuevos, recuperados, total_ok).

    caidos_nuevos / recuperados = listas de (nombre, url, detalle) para el aviso."""
    caidos, recuperados, ok_total = [], [], 0
    urls = {e['url'] for e in lista}
    for url in list(memoria):
        if url not in urls:
            del memoria[url]  # ya no está en el proyecto
    for e in lista:
        url = e['url']
        ok, detalle = probar_fn(url)
        m = memoria.setdefault(url, {'fallos': 0, 'avisado': False})
        if ok:
            ok_total += 1
            if m['avisado']:
                recuperados.append((e.get('nombre', url), url, detalle))
            m['fallos'], m['avisado'] = 0, False
        else:
            m['fallos'] += 1
            if m['fallos'] >= fallos_para_avisar and not m['avisado']:
                caidos.append((e.get('nombre', url), url, detalle))
                m['avisado'] = True
    return caidos, recuperados, ok_total
