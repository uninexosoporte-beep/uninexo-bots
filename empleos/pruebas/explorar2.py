import re, html, sys, json, urllib.request, urllib.parse, http.cookiejar
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'
def limpio(x): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip()
U = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/modalidades_formativas.xhtml'
H = {'Faces-Request': 'partial/ajax', 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)); op.addheaders = [('User-Agent', UA)]
p = op.open(U, timeout=60).read().decode('utf-8', 'ignore')
i = p.find('titulo-vacante', p.find('</style>'))
print('inicial: bloques con titulo-vacante fuera del CSS =', p.count('class="titulo-vacante'))
print('opciones modalidad:', re.findall(r'data-label="([^"]+)"', p)[:12])
vs = re.search(r'name="javax.faces.ViewState"[^>]*value="([^"]+)"', p).group(1)
btns = re.findall(r'<button id="(frmLstModFormativas:j_idt\d+)"([^>]*)>', p)
for b, a in btns[:6]:
    print('boton', b, '|', limpio(a)[:80])
btn = [b for b, a in btns if 'btn-sensitive' in a]
print('btn-sensitive:', btn)
def post(source, extra):
    data = {'javax.faces.partial.ajax': 'true', 'javax.faces.source': source, 'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'frmLstModFormativas', source: source, 'frmLstModFormativas': 'frmLstModFormativas',
            'frmLstModFormativas:cboDep_focus': '', 'javax.faces.ViewState': vs}
    data.update(extra)
    return op.open(urllib.request.Request(U, data=urllib.parse.urlencode(data).encode(), headers=H), timeout=120).read().decode('utf-8', 'ignore')
r = post(btn[0] if btn else btns[0][0], {'frmLstModFormativas:cboDep_input': '17'})
print('respuesta KB', len(r) // 1024, '| bloques:', r.count('class="titulo-vacante'), '| puestos:', re.search(r'(\d+) (?:puesto|oferta|vacante)\S* encontrad', limpio(r)))
j = r.find('class="titulo-vacante')
print('--- bloque:', limpio(r[j - 200:j + 2500])[:900])
print('=== respuesta (texto) ===')
print(limpio(r)[:1800])
print('=== clases presentes ===')
print(sorted(set(re.findall(r'class="([a-z\-]+(?:vacante|entidad|detalle|titulo)[a-z\-]*)', r)))[:20])
open('resp_practicas.xml', 'w', encoding='utf-8').write(r)
