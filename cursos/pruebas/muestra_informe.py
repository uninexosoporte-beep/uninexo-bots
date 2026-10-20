"""Genera el informe de cursos con candidatas de muestra y lo guarda como HTML + imagen para revisar el diseño."""
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

with open(os.path.join(AQUI, 'config.json'), encoding='utf-8') as f:
    cfg = json.load(f)
hoy = date(2026, 10, 7)


def c(name, tipo, inst, slug, area, gratis, costo, limite, modalidad, fecha):
    return {'name': name, 'tipo': tipo, 'institucion': inst, 'slug': slug, 'enlaceOficial': f'https://www.gob.pe/institucion/{slug}/campa%C3%B1as/0-muestra', 'fecha': fecha,
            'fuente': 'gobpe-campañas', 'area': area, 'region': 'Todo el país', 'gratuito': gratis, 'costo': costo, 'fechaLimite': limite, 'modalidad': modalidad, 'descripcion': ''}


cands = [
    c('Curso Online Gratuito de Quechua Central', 'curso', 'Ministerio de Cultura', 'cultura', 'Idiomas', True, None, '2026-11-25', 'virtual', '2026-09-30'),
    c('Curso virtual: Manejo Integrado de Cultivos Tropicales: Café y Cacao', 'curso', 'INIA', 'inia', 'Agropecuaria y Ambiente', None, None, None, 'virtual', '2026-09-11'),
    c('Beca de ejemplo: Maestría en Gestión Pública', 'beca', 'PRONABEC', 'pronabec', 'Gestión Pública', False, 'S/ 350', '2026-10-10', 'presencial', '2026-10-05'),
    c('Eventos y charlas gratuitas del MTPE', 'webinar', 'Ministerio de Trabajo (MTPE)', 'mtpe', 'Empleabilidad y Desarrollo Personal', True, None, None, None, '2026-09-01'),
]
cambios = [{'nombre': 'OEA · becas académicas', 'url': 'https://www.oas.org/es/becas/', 'lineas': ['Abierta la convocatoria 2027 del Programa de Becas Académicas']}]
h = informe.construir_html(hoy, cands, cambios, [], cfg)
ruta = os.path.join(AQUI, 'pruebas', 'informe_muestra.html')
with open(ruta, 'w', encoding='utf-8') as f:
    f.write(h)
png = os.path.join(AQUI, 'pruebas', 'informe_muestra.png')
subprocess.run([informe.buscar_navegador(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=820,1300', f'--screenshot={png}', Path(ruta).as_uri()],
               timeout=90, capture_output=True)
print('PNG:', png, os.path.exists(png))
