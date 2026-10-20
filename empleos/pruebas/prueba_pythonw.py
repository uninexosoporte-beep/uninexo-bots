"""Se ejecuta con pythonw.exe (sin ventana, como lo hace el programador de Windows) para comprobar que el PDF se crea en ese modo."""
import json
import os
import sys
import traceback
from datetime import date

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
SALIDA = os.path.join(AQUI, 'pruebas', 'resultado_pythonw.txt')
try:
    import informe
    import seleccion
    with open(os.path.join(AQUI, 'config.json'), encoding='utf-8') as f:
        cfg = json.load(f)
    r = seleccion.convertir({'cargo': 'ABOGADO', 'entidad': 'PODER JUDICIAL', 'ubicacion': 'CUSCO - CUSCO', 'numero': 'D.LEG 1057 - DETERMINADO (NECESIDAD TRANSITORIA)-1',
                             'vacantes': '1', 'remuneracion': 'S/. 3,000.00', 'fin': '31/12/2026', 'inicio': '', 'modalidad': ''}, 'servir-ofertas', 'Cusco')
    ruta = os.path.join(AQUI, 'pruebas', 'prueba_pythonw.pdf')
    informe.html_a_pdf(informe.construir_html(date(2026, 10, 7), {'Cusco': [r]}, {}, [], [], [], cfg, set()), ruta)
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write(f'OK sys.stdout={sys.stdout!r} pdf={os.path.getsize(ruta)} bytes')
except Exception:
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write('ERROR\n' + traceback.format_exc())
