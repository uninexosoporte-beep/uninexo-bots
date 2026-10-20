import re, html, sys, json, urllib.request, urllib.parse, http.cookiejar
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
def limpio(x): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
# (1) SERVIR prácticas: formulario, región y primer bloque
U = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/modalidades_formativas.xhtml'
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)); op.addheaders = [('User-Agent', UA)]
p = op.open(U, timeout=60).read().decode('utf-8', 'ignore')
print('forms:', re.findall(r'<form id="([^"]+)"', p))
print('inputs cbo:', re.findall(r'id="([^"]*cbo[^"]*)"', p)[:8])
print('botones:', re.findall(r'<button id="([^"]+)"[^>]*>', p)[:5])
bl = p.split('cuadro-vacantes')[1:3]
for b in bl[:1]:
    print('--- primer bloque (texto):', limpio(b)[:500])
    print('--- pares etiqueta/valor:', re.findall(r'([^<>:]{3,40}):</span>\s*<span class="detalle-sp">(.*?)</span>', b, re.S)[:8])
# (3) listado por tipo en una institución
for u in ['https://www.gob.pe/institucion/sunarp/informes-publicaciones/tipos/80-convocatoria-de-trabajo',
          'https://www.gob.pe/institucion/ugelcoronelportillo/informes-publicaciones/tipos/80-convocatoria-de-trabajo']:
    try:
        t = op.open(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=60).read().decode('utf-8', 'ignore')
        ids = re.findall(r'href="(/institucion/[^"]+/informes-publicaciones/(\d+)-[^"]*)"', t)
        print('(3)', u[-70:], '| KB', len(t) // 1024, '| enlaces con id:', len(set(i for _, i in ids)), '| fechas:', re.findall(r'\d{1,2} de [a-záéíóú]+ de 20\d\d', t)[:5])
    except Exception as e:
        print('(3)', u[-70:], 'ERROR', repr(e)[:80])
