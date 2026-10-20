"""Informe diario en PDF del bot de Cursos: se arma como página web (HTML) y Microsoft Edge o Chrome, que ya están en tu PC, la convierten en PDF."""
import html
import os
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from clasificar import TIPO_ETIQUETA
from seleccion import prioridad

NAVEGADORES = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
]
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
ORDEN_TIPOS = ['beca', 'especializacion', 'diplomado', 'curso', 'certificacion', 'taller', 'webinar', 'voluntariado', 'experiencia_laboral', 'convocatoria']

CSS = '''
@page { size: A4; margin: 12mm 12mm 14mm 12mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937; font-size: 10pt; line-height: 1.35; margin: 0; }
header { background: #0f766e; color: #fff; padding: 14px 18px; border-radius: 10px; }
h1 { font-size: 18pt; margin: 0 0 2px; }
.sub { font-size: 10pt; opacity: .92; }
.chips { margin-top: 8px; }
.chips span { display: inline-block; background: rgba(255,255,255,.2); border-radius: 999px; padding: 2px 11px; margin: 4px 6px 0 0; font-size: 9.5pt; }
h2 { font-size: 13pt; color: #115e59; border-bottom: 2px solid #99f6e4; padding-bottom: 3px; margin: 20px 0 6px; page-break-after: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.2pt; }
th { text-align: left; background: #f0fdfa; color: #115e59; padding: 5px 6px; font-size: 8.8pt; }
td { padding: 6px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }
tr { page-break-inside: avoid; }
.nombre { font-weight: 700; }
.ent { color: #4b5563; }
.pronto { color: #b91c1c; font-weight: 700; }
.gratis { color: #047857; font-weight: 700; }
.nota { background: #f9fafb; border-left: 3px solid #5eead4; padding: 6px 10px; font-size: 9pt; color: #374151; margin: 10px 0; }
ul { margin: 4px 0 8px 16px; padding: 0; } li { margin: 3px 0; }
a { color: #0f766e; text-decoration: none; }
.area { color: #0f766e; font-size: 8.8pt; }
.pie { margin-top: 22px; font-size: 8.5pt; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 6px; }
.error { background: #fef2f2; border-left: 3px solid #f87171; padding: 6px 10px; font-size: 9pt; color: #7f1d1d; margin: 10px 0; }
'''


class ErrorInforme(Exception):
    pass


def e(x):
    return html.escape(str(x if x is not None else ''), quote=True)


def fecha_bonita(hoy):
    return f'{DIAS[hoy.weekday()]} {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'


def corta(iso):
    return f'{iso[8:10]}/{iso[5:7]}'


def costo_texto(c):
    if c['gratuito'] is True:
        return '<span class="gratis">Gratis</span>'
    if c['costo']:
        return e(c['costo'])
    return '<span class="ent">Por confirmar</span>'


def _fila(c, hoy):
    if c['fechaLimite']:
        dias = (date.fromisoformat(c['fechaLimite']) - hoy).days
        clase = ' class="pronto"' if dias <= 5 else ''
        cierre = f'<td{clase}>{corta(c["fechaLimite"])}<br>{dias} {"día" if dias == 1 else "días"}</td>'
    else:
        cierre = '<td class="ent">Sin fecha en la página</td>'
    mod = {'virtual': 'Virtual', 'presencial': 'Presencial', 'hibrido': 'Híbrido'}.get(c['modalidad'] or '', '—')
    area = f'<div class="area">{e(c["area"])}</div>' if c['area'] != 'Todas las carreras' else ''
    return (f'<tr><td><div class="nombre"><a href="{e(c["enlaceOficial"])}">{e(c["name"])}</a></div><div class="ent">{e(c["institucion"])}</div>{area}</td>'
            f'<td>{costo_texto(c)}</td>{cierre}<td>{mod}</td><td>{e(corta(c["fecha"]))}</td></tr>')


def _seccion_candidatos(candidatos, hoy):
    por_tipo = {}
    for c in sorted(candidatos, key=prioridad):
        por_tipo.setdefault(c['tipo'], []).append(c)
    partes = []
    for tipo in ORDEN_TIPOS:
        lista = por_tipo.get(tipo)
        if not lista:
            continue
        partes.append(f'<h2>{e(TIPO_ETIQUETA[tipo])} · {len(lista)}</h2>')
        partes.append('<table><tr><th style="width:50%">Nombre e institución</th><th>Costo</th><th>Cierra</th><th>Modalidad</th><th>Publicada</th></tr>'
                      + ''.join(_fila(c, hoy) for c in lista) + '</table>')
    return '\n'.join(partes)


def _seccion_paginas(cambios):
    if not cambios:
        return ''
    partes = [f'<h2>🔔 Páginas vigiladas con novedades · {len(cambios)}</h2>']
    for c in cambios:
        lis = ''.join(f'<li>{e(l[:200])}</li>' for l in c['lineas'][:8])
        partes.append(f'<h3 style="font-size:11pt;margin:12px 0 2px"><a href="{e(c["url"])}">{e(c["nombre"])}</a></h3><ul>{lis}</ul>')
    return '\n'.join(partes)


def _filtros_texto(cfg):
    r = cfg.get('reglas') or {}
    t, a, i = r.get('tipos') or {}, r.get('areas') or {}, r.get('instituciones') or {}
    partes = ['Tipos: ' + (', '.join(t['solo']) if t.get('solo') else 'todos'), 'Áreas: ' + (', '.join(a['solo']) if a.get('solo') else 'todas')]
    if r.get('solo_gratuitos'):
        partes.append('solo gratuitos' + (' o sin precio indicado' if r.get('incluir_costo_desconocido', True) else ''))
    if i.get('incluir'):
        partes.append('incluye: ' + ', '.join(i['incluir']))
    return ' · '.join(partes)


def construir_html(hoy, candidatos, cambios_paginas, errores, cfg):
    def pl(n, uno, varios):
        return f'{n} {uno if n == 1 else varios}'
    gratis = sum(1 for c in candidatos if c['gratuito'] is True)
    chips = [pl(len(candidatos), 'oportunidad nueva', 'oportunidades nuevas'), pl(gratis, 'gratuita', 'gratuitas'), pl(len(cambios_paginas), 'página con cambios', 'páginas con cambios')]
    cuerpo = [
        f'<header><h1>Cursos y Oportunidades · UniNexo</h1><div class="sub">Informe del {e(fecha_bonita(hoy))}</div>'
        f'<div class="chips">{"".join(f"<span>{e(c)}</span>" for c in chips)}</div></header>',
        '<div class="nota">Son <b>candidatas</b> que el bot encontró en páginas del Estado: aún nadie las revisó. Abre cada enlace, confirma el costo y las fechas en la página oficial '
        'y, si sirven, impórtalas desde el botón «Importar del bot» de la sección Cursos para aprobarlas.</div>',
        _seccion_candidatos(candidatos, hoy),
        _seccion_paginas(cambios_paginas),
    ]
    if errores:
        cuerpo.append('<div class="error"><b>No pude leer:</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in errores[:12]) + '</ul></div>')
    cuerpo.append(f'<div class="pie">Filtros activos → {e(_filtros_texto(cfg))}.<br>Informe generado por el bot de cursos de UniNexo con datos públicos de gob.pe. '
                  '«Por confirmar» significa que la página no dice el costo. Las oportunidades listas para importar van en el archivo .json que llega junto a este PDF.</div>')
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Cursos y Oportunidades {hoy.isoformat()}</title><style>{CSS}</style></head><body>{"".join(cuerpo)}</body></html>'


def buscar_navegador():
    forzado = os.environ.get('UNINEXO_NAVEGADOR')
    for ruta in ([forzado] if forzado else []) + NAVEGADORES:
        if ruta and os.path.exists(ruta):
            return ruta
    raise ErrorInforme('No encontré Microsoft Edge ni Google Chrome para crear el PDF')


def html_a_pdf(html_texto, ruta_pdf, timeout=120):
    """Convierte el HTML en PDF con Edge/Chrome sin ventana. Devuelve la ruta del PDF."""
    navegador = buscar_navegador()
    trabajo = tempfile.mkdtemp(prefix='uninexo-pdf-cursos-')
    try:
        ruta_html = os.path.join(trabajo, 'informe.html')
        with open(ruta_html, 'w', encoding='utf-8') as f:
            f.write(html_texto)
        if os.path.exists(ruta_pdf):
            os.remove(ruta_pdf)
        for modo in ('--headless=new', '--headless'):
            cmd = [navegador, modo, '--disable-gpu', '--no-first-run', f'--user-data-dir={os.path.join(trabajo, "perfil")}',
                   '--no-pdf-header-footer', f'--print-to-pdf={ruta_pdf}', Path(ruta_html).as_uri()]
            try:
                # stdin=DEVNULL: sin ventana (pythonw) Windows no tiene entrada estándar y el proceso hijo fallaría
                subprocess.run(cmd, timeout=timeout, capture_output=True, stdin=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            except subprocess.TimeoutExpired:
                continue
            if os.path.exists(ruta_pdf) and os.path.getsize(ruta_pdf) > 1500:
                return ruta_pdf
        raise ErrorInforme('El navegador no pudo crear el PDF')
    finally:
        shutil.rmtree(trabajo, ignore_errors=True)
