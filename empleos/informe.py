"""Informe diario en PDF: se arma como una página web bonita (HTML) y Microsoft Edge o Chrome, que ya están en tu PC, la convierten en PDF.
No necesita instalar nada. Si no hay navegador o falla, el bot vuelve a mandar los mensajes de siempre."""
import html
import os
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

import mensajes
import reglas
from seleccion import URL_SERVIR_OFERTAS, URL_SERVIR_PRACTICAS, fecha_larga

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
.chips span { display: inline-block; background: rgba(255,255,255,.18); border-radius: 999px; padding: 2px 11px; margin: 4px 6px 0 0; font-size: 9.5pt; }
h2 { font-size: 13pt; color: #312e81; border-bottom: 2px solid #c7d2fe; padding-bottom: 3px; margin: 20px 0 6px; page-break-after: avoid; }
h3 { font-size: 11pt; color: #3730a3; margin: 14px 0 4px; page-break-after: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.2pt; }
th { text-align: left; background: #eef2ff; color: #3730a3; padding: 5px 6px; font-size: 8.8pt; }
td { padding: 6px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }
tr { page-break-inside: avoid; }
.cargo { font-weight: 700; }
.ent { color: #4b5563; }
.pronto { color: #b91c1c; font-weight: 700; }
.car { color: #4338ca; font-size: 8.8pt; }
.nota { background: #f9fafb; border-left: 3px solid #a5b4fc; padding: 6px 10px; font-size: 9pt; color: #374151; margin: 10px 0; }
.amp { background: #fef3c7; color: #92400e; border-radius: 4px; padding: 0 5px; font-size: 8.5pt; font-weight: 700; }
ul { margin: 4px 0 8px 16px; padding: 0; } li { margin: 3px 0; }
a { color: #4338ca; text-decoration: none; }
.pie { margin-top: 22px; font-size: 8.5pt; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 6px; }
.error { background: #fef2f2; border-left: 3px solid #f87171; padding: 6px 10px; font-size: 9pt; color: #7f1d1d; margin: 10px 0; }
'''


class ErrorInforme(Exception):
    pass


def e(x):
    return html.escape(str(x if x is not None else ''), quote=True)


def fecha_bonita(hoy):
    return f'{DIAS[hoy.weekday()]} {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'


def _tabla_plazas(recs, hoy, ampliadas):
    filas = []
    for r in recs:
        dias = mensajes.dias_para(r['cierre'], hoy)
        clase = ' class="pronto"' if dias <= 5 else ''
        amp = '<span class="amp">AMPLIADA</span> ' if r['clave_base'] in ampliadas else ''
        sueldo = f'S/ {r["sueldo"]:,.0f}' if r.get('sueldo') else '—'
        carrera = f'<div class="car">🎓 {e(reglas.etiqueta_carreras(r["carreras"]))}</div>' if r.get('carreras') else ''
        filas.append(
            f'<tr><td>{amp}<div class="cargo">{e(r["cargo"])}</div><div class="ent">{e(r["institucion"])}</div>{carrera}</td>'
            f'<td>{sueldo}</td>'
            f'<td{clase}>{e(fecha_larga(r["cierre"])[:5])}<br>{dias} {"día" if dias == 1 else "días"}</td>'
            f'<td>{e(mensajes.numero_corto(r))}<br><span class="ent">{e(r["vacantes"])} {"vacante" if r["vacantes"] == 1 else "vacantes"}</span></td>'
            f'<td>{e(r["distrito"])}</td></tr>')
    return ('<table><tr><th style="width:45%">Cargo y entidad</th><th>Sueldo</th><th>Cierra</th><th>Tipo y N.º de convocatoria</th><th>Lugar</th></tr>'
            + ''.join(filas) + '</table>')


def _seccion_plazas(titulo, por_region, hoy, ampliadas, cfg, enlace):
    if not por_region:
        return ''
    total = sum(len(v) for v in por_region.values())
    partes = [f'<h2>{e(titulo)} · {total}</h2>']
    for region in reglas.orden_regiones(por_region, cfg):
        estrella = '⭐ ' if reglas.es_prioritaria(region, cfg) else ''
        partes.append(f'<h3>📍 {estrella}{e(region)} ({len(por_region[region])})</h3>')
        partes.append(_tabla_plazas(por_region[region], hoy, ampliadas))
    partes.append(f'<div class="nota">Cómo postular: entra a <a href="{enlace}">SERVIR · Talento Perú</a>, elige la <b>Ubicación</b> (la región), '
                  'busca la entidad y el <b>número de convocatoria</b> de la tabla, y descarga las bases en Word. Postula siempre desde el portal oficial; es gratis.</div>')
    return '\n'.join(partes)


def _seccion_gobpe(items, hoy):
    if not items:
        return ''
    por_inst = {}
    for it in sorted(items, key=lambda x: x['fecha'], reverse=True):
        por_inst.setdefault(it['institucion'], []).append(it)
    partes = [f'<h2>📄 Anuncios de convocatorias en gob.pe · {len(items)}</h2>',
              '<div class="nota">Estos anuncios no traen fecha de cierre en la lista: abre cada enlace y revisa las bases.</div>']
    for inst, lista in sorted(por_inst.items(), key=lambda kv: -len(kv[1])):
        lis = []
        for it in lista[:12]:
            hace = (hoy - date.fromisoformat(it['fecha'])).days
            cuando = 'hoy' if hace <= 0 else ('ayer' if hace == 1 else f'hace {hace} días')
            lis.append(f'<li><a href="{e(it["url"])}">{e(it["titulo"][:160])}</a> · {cuando}</li>')
        if len(lista) > 12:
            lis.append(f'<li>… y {len(lista) - 12} más de {e(inst)}</li>')
        partes.append(f'<h3>🏛 {e(inst)} ({len(lista)})</h3><ul>{"".join(lis)}</ul>')
    return '\n'.join(partes)


def _seccion_paginas(cambios):
    if not cambios:
        return ''
    partes = [f'<h2>🔔 Páginas vigiladas con novedades · {len(cambios)}</h2>']
    for c in cambios:
        lis = ''.join(f'<li>{e(l[:200])}</li>' for l in c['lineas'][:8])
        partes.append(f'<h3><a href="{e(c["url"])}">{e(c["nombre"])}</a></h3><ul>{lis}</ul>')
    return '\n'.join(partes)


def _filtros_texto(cfg):
    r = (cfg.get('reglas') or {})
    car, reg = r.get('carreras') or {}, r.get('regiones') or {}
    partes = []
    partes.append('Carreras: ' + (', '.join(car['solo']) if car.get('solo') else 'todas'))
    if car.get('ignorar'):
        partes.append('sin: ' + ', '.join(car['ignorar']))
    partes.append('Regiones: ' + (', '.join(reg['solo']) if reg.get('solo') else 'todas'))
    if reg.get('ignorar'):
        partes.append('sin: ' + ', '.join(reg['ignorar']))
    f = cfg['filtros']
    partes.append(f'abiertas al menos {f["dias_minimos_abierta"]} días · máx. {f["max_por_region"]} por región')
    return ' · '.join(partes)


def construir_html(hoy, nuevas_servir, nuevas_practicas, nuevos_gobpe, cambios_paginas, errores, cfg, ampliadas=()):
    n1, n2 = sum(len(v) for v in nuevas_servir.values()), sum(len(v) for v in nuevas_practicas.values())
    def pl(n, uno, varios):
        return f'{n} {uno if n == 1 else varios}'
    chips = [pl(n1, 'plaza nueva', 'plazas nuevas'), pl(n2, 'práctica', 'prácticas'), pl(len(nuevos_gobpe), 'anuncio en gob.pe', 'anuncios en gob.pe'),
             pl(len(cambios_paginas), 'página con cambios', 'páginas con cambios')]
    cuerpo = [
        f'<header><h1>Empleos del Estado · UniNexo</h1><div class="sub">Informe del {e(fecha_bonita(hoy))}</div>'
        f'<div class="chips">{"".join(f"<span>{e(c)}</span>" for c in chips)}</div></header>',
        _seccion_plazas('🆕 Nuevas plazas en el Estado', nuevas_servir, hoy, ampliadas, cfg, URL_SERVIR_OFERTAS),
        _seccion_plazas('🎓 Nuevas prácticas', nuevas_practicas, hoy, ampliadas, cfg, URL_SERVIR_PRACTICAS),
        _seccion_gobpe(nuevos_gobpe, hoy),
        _seccion_paginas(cambios_paginas),
    ]
    if errores:
        cuerpo.append('<div class="error"><b>No pude leer:</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in errores[:12]) + '</ul></div>')
    cuerpo.append(f'<div class="pie">Filtros activos → {e(_filtros_texto(cfg))}.<br>Informe generado por el bot de empleos de UniNexo con datos públicos de SERVIR y gob.pe. '
                  'Verifica siempre las bases en el portal oficial antes de postular. Las plazas listas para publicar van en el archivo .json que llega junto a este PDF.</div>')
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Empleos del Estado {hoy.isoformat()}</title><style>{CSS}</style></head><body>{"".join(cuerpo)}</body></html>'


def buscar_navegador():
    forzado = os.environ.get('UNINEXO_NAVEGADOR')
    for ruta in ([forzado] if forzado else []) + NAVEGADORES:
        if ruta and os.path.exists(ruta):
            return ruta
    raise ErrorInforme('No encontré Microsoft Edge ni Google Chrome para crear el PDF')


def html_a_pdf(html_texto, ruta_pdf, timeout=120):
    """Convierte el HTML en PDF con Edge/Chrome sin ventana. Devuelve la ruta del PDF."""
    navegador = buscar_navegador()
    trabajo = tempfile.mkdtemp(prefix='uninexo-pdf-')
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
