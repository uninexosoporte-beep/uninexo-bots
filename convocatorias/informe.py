"""Informe diario en PDF del bot de Convocatorias: se arma como página web (HTML) y Microsoft Edge o Chrome, que ya están en tu PC, la convierten en PDF."""
import html
import os
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from clasificar import TIPO_ETIQUETA
from seleccion import ORDEN_TIPOS, prioridad

NAVEGADORES = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
]
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

CSS = '''
@page { size: A4; margin: 12mm 12mm 14mm 12mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937; font-size: 10pt; line-height: 1.35; margin: 0; }
header { background: #4338ca; color: #fff; padding: 14px 18px; border-radius: 10px; }
h1 { font-size: 18pt; margin: 0 0 2px; }
.sub { font-size: 10pt; opacity: .92; }
.chips { margin-top: 8px; }
.chips span { display: inline-block; background: rgba(255,255,255,.2); border-radius: 999px; padding: 2px 11px; margin: 4px 6px 0 0; font-size: 9.5pt; }
h2 { font-size: 13pt; color: #3730a3; border-bottom: 2px solid #c7d2fe; padding-bottom: 3px; margin: 20px 0 6px; page-break-after: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.2pt; }
th { text-align: left; background: #eef2ff; color: #3730a3; padding: 5px 6px; font-size: 8.8pt; }
td { padding: 6px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }
tr { page-break-inside: avoid; }
.nombre { font-weight: 700; }
.ent { color: #4b5563; }
.pronto { color: #b91c1c; font-weight: 700; }
.gratis { color: #047857; font-weight: 700; }
.nota { background: #f9fafb; border-left: 3px solid #a5b4fc; padding: 6px 10px; font-size: 9pt; color: #374151; margin: 10px 0; }
ul { margin: 4px 0 8px 16px; padding: 0; } li { margin: 3px 0; }
a { color: #4338ca; text-decoration: none; }
.area { color: #4338ca; font-size: 8.8pt; }
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


def _fila(c, hoy):
    if c['fechaLimite']:
        dias = (date.fromisoformat(c['fechaLimite']) - hoy).days
        clase = ' class="pronto"' if dias <= 5 else ''
        cierre = f'<td{clase}>{corta(c["fechaLimite"])}<br>{dias} {"día" if dias == 1 else "días"}</td>'
    else:
        cierre = '<td class="ent">Sin fecha en la página</td>'
    mod = {'virtual': 'Virtual', 'presencial': 'Presencial', 'hibrido': 'Híbrido'}.get(c['modalidad'] or '', '—')
    nueva = '<div class="area">Entidad nueva en UniNexo</div>' if c.get('entidad') else ''
    return (f'<tr><td><div class="nombre"><a href="{e(c["enlaceOficial"])}">{e(c["name"])}</a></div><div class="ent">{e(c["institucion"])}</div>{nueva}</td>'
            f'{cierre}<td>{mod}</td><td>{e(c["region"])}</td><td>{e(corta(c["fecha"]))}</td></tr>')


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
        partes.append('<table><tr><th style="width:46%">Nombre e institución</th><th>Cierra</th><th>Modalidad</th><th>Lugar</th><th>Publicada</th></tr>'
                      + ''.join(_fila(c, hoy) for c in lista) + '</table>')
    return '\n'.join(partes)


def _seccion_paginas(cambios):
    if not cambios:
        return ''
    partes = [f'<h2>🔔 Programas vigilados con novedades · {len(cambios)}</h2>']
    for c in cambios:
        lis = ''.join(f'<li>{e(l[:200])}</li>' for l in c['lineas'][:8])
        partes.append(f'<h3 style="font-size:11pt;margin:12px 0 2px"><a href="{e(c["url"])}">{e(c["nombre"])}</a></h3><ul>{lis}</ul>')
    return '\n'.join(partes)


def _filtros_texto(cfg):
    r = cfg.get('reglas') or {}
    tp, i = r.get('tipos') or {}, r.get('instituciones') or {}
    partes = ['Tipos: ' + (', '.join(tp['solo']) if tp.get('solo') else 'todos'), 'ignora: ' + (', '.join(tp['ignorar']) if tp.get('ignorar') else 'ninguno')]
    if i.get('incluir'):
        partes.append('incluye: ' + ', '.join(i['incluir']))
    return ' · '.join(partes)


def construir_html(hoy, candidatos, cambios_paginas, errores, cfg):
    def pl(n, uno, varios):
        return f'{n} {uno if n == 1 else varios}'
    entidades = sum(1 for c in candidatos if c.get('entidad'))
    chips = [pl(len(candidatos), 'convocatoria nueva', 'convocatorias nuevas'), pl(entidades, 'entidad nueva', 'entidades nuevas'), pl(len(cambios_paginas), 'programa con cambios', 'programas con cambios')]
    cuerpo = [
        f'<header><h1>Convocatorias · UniNexo</h1><div class="sub">Informe del {e(fecha_bonita(hoy))}</div>'
        f'<div class="chips">{"".join(f"<span>{e(c)}</span>" for c in chips)}</div></header>',
        '<div class="nota">Son <b>candidatas</b> que el bot encontró en páginas del Estado: aún nadie las revisó. Abre cada enlace, confirma fechas y requisitos en la página oficial '
        'y, si sirven, impórtalas desde el botón «Importar del bot» de la pestaña Convocatorias.</div>',
        _seccion_candidatos(candidatos, hoy),
        _seccion_paginas(cambios_paginas),
    ]
    if errores:
        cuerpo.append('<div class="error"><b>No pude leer:</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in errores[:12]) + '</ul></div>')
    cuerpo.append(f'<div class="pie">Filtros activos → {e(_filtros_texto(cfg))}.<br>Informe generado por el bot de convocatorias de UniNexo con datos públicos de gob.pe. '
                  'Una «entidad nueva» es una entidad que publica convocatorias de prácticas y aún no está en UniNexo. Lo listo para importar va en el archivo .json que llega junto a este PDF.</div>')
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Convocatorias {hoy.isoformat()}</title><style>{CSS}</style></head><body>{"".join(cuerpo)}</body></html>'


def buscar_navegador():
    forzado = os.environ.get('UNINEXO_NAVEGADOR')
    for ruta in ([forzado] if forzado else []) + NAVEGADORES:
        if ruta and os.path.exists(ruta):
            return ruta
    raise ErrorInforme('No encontré Microsoft Edge ni Google Chrome para crear el PDF')


def html_a_pdf(html_texto, ruta_pdf, timeout=120):
    """Convierte el HTML en PDF con Edge/Chrome sin ventana. Devuelve la ruta del PDF."""
    navegador = buscar_navegador()
    trabajo = tempfile.mkdtemp(prefix='uninexo-pdf-convocatorias-')
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
