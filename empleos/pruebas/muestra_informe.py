"""Genera el informe con datos de muestra reales (de SERVIR) y lo guarda como HTML + imagen para revisar el diseño."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.stdout.reconfigure(encoding='utf-8')
import informe
import seleccion
import servir

cfg = json.load(open(os.path.join(AQUI, 'config.json'), encoding='utf-8'))
hoy = date(2026, 10, 7)
por_region = {}
for nombre, codigo in (('Madre de Dios', '17'), ('Arequipa', '04')):
    _, _, crudas = servir.leer_region(codigo, 1, 1)
    for o in crudas:
        r = seleccion.convertir(o, 'servir-ofertas', nombre)
        if r and not seleccion.motivo_descarte(r, cfg, hoy):
            por_region.setdefault(nombre, []).append(r)
for k in por_region:
    por_region[k] = por_region[k][:4]
gob = [{'titulo': 'Proceso CAS N° 017-2026- Digitador- SUNARP-ZRN°XI', 'url': 'https://www.gob.pe/institucion/sunarp/informes-publicaciones/8694523-x', 'fecha': '2026-10-07',
        'institucion': 'SUNARP', 'slug': 'sunarp', 'fuente': 'gobpe'},
       {'titulo': 'Convocatoria Practicas N° 064-2026 PRACTICANTE PROFESIONAL - OEE', 'url': 'https://www.gob.pe/institucion/indecopi/informes-publicaciones/8633739-x',
        'fecha': '2026-10-06', 'institucion': 'INDECOPI', 'slug': 'indecopi', 'fuente': 'gobpe'}]
cambios = [{'nombre': 'SUNARP · concursos públicos de méritos', 'url': 'https://www.gob.pe/institucion/sunarp/colecciones/2164-x', 'lineas': ['Concurso Público de Méritos N°01-2026 | https://…']}]
h = informe.construir_html(hoy, por_region, {}, gob, cambios, [], cfg, set())
ruta = os.path.join(AQUI, 'pruebas', 'informe_muestra.html')
open(ruta, 'w', encoding='utf-8').write(h)
png = os.path.join(AQUI, 'pruebas', 'informe_muestra.png')
subprocess.run([informe.buscar_navegador(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=820,1500',
                f'--screenshot={png}', Path(ruta).as_uri()], timeout=90, capture_output=True)
print('HTML:', ruta, '| PNG:', png, os.path.exists(png))
