"""Pruebas del bot (sin internet). Correr con:  python -m unittest discover -s tests -v   (desde D:\\uninexo-bot)"""
import json
import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import almacen  # noqa: E402
import gobpe  # noqa: E402
import mensajes  # noqa: E402
import normalizar  # noqa: E402
import publicado  # noqa: E402
import seleccion  # noqa: E402
import servir  # noqa: E402
import telegram  # noqa: E402
import vigilante  # noqa: E402

HOY = date(2026, 10, 7)
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json'), encoding='utf-8') as _f:
    CFG = json.load(_f)
CAS = 'D.LEG 1057 - DETERMINADO (NECESIDAD TRANSITORIA)'


def cruda(cargo='ESPECIALISTA EN CONTABILIDAD', entidad='MUNICIPALIDAD DISTRITAL DE SAN PABLO', ubic='CUSCO - SAN PABLO', numero=CAS + '-8',
          vac='1', sueldo='S/. 3,500.00', fin='21/10/2026'):
    return {'cargo': cargo, 'entidad': entidad, 'ubicacion': ubic, 'numero': numero, 'vacantes': vac, 'remuneracion': sueldo, 'inicio': '', 'fin': fin, 'modalidad': ''}


def rec(**kw):
    return seleccion.convertir(cruda(**kw), 'servir-ofertas', 'Cusco')


class TestNormalizar(unittest.TestCase):
    def test_texto_en_mayusculas_queda_legible(self):
        p = normalizar.propios_departamentos()
        self.assertEqual(normalizar.entidad_final('MUNICIPALIDAD DISTRITAL DE SAN PABLO', p), 'Municipalidad Distrital de San Pablo')
        self.assertEqual(normalizar.cargo_final('ESPECIALISTA EN GESTION DE RIESGOS', p), 'Especialista en gestión de riesgos')
        self.assertEqual(normalizar.cargo_final('TECNICO EN ENFERMERIA', p), 'Técnico en enfermería')
        self.assertEqual(normalizar.entidad_final('MUNIC. DISTRITAL DE ILO', p), 'Municipalidad Distrital de Ilo')

    def test_errores_de_tipeo_y_abreviaturas_del_portal(self):
        p = normalizar.propios_departamentos()
        self.assertEqual(normalizar.cargo_final('ESPECIALISTA ADMISNITRATIVO', p), 'Especialista administrativo')
        self.assertEqual(normalizar.entidad_final('DIRECC. REGIONAL DE SALUD MADRE DE DIOS', p), 'Dirección Regional de Salud Madre de Dios')
        self.assertEqual(normalizar.entidad_final('MINIST. DE TRABAJO Y PROMOCION DEL EMPLEO', p), 'Ministerio de Trabajo y Promoción del Empleo')

    def test_correcciones_conocidas_y_siglas(self):
        p = normalizar.propios_departamentos()
        self.assertEqual(normalizar.entidad_final('ZONA REGISTRAL NRO XI SEDE ICA', p), 'Zona Registral N° XI - Sede Ica')
        self.assertEqual(normalizar.cargo_final('RESPONSABLE DE BIENESTAR S.R.E.', p), 'Responsable de bienestar SRE')
        self.assertIn('INPE', normalizar.entidad_final('INPE OFICINA REGIONAL ALTIPLANO PUNO', p))

    def test_cargos_largos_se_resumen(self):
        p = normalizar.propios_departamentos()
        c = normalizar.cargo_final('CONTRATACIÓN ADMINISTRATIVA DE SERVICIOS DE UN(A) DOCENTE PARA LA ENSEÑANZA DE LA ASIGNATURA DE INGLÉS PARA EL COLEGIO DE ALTO RENDIMIENTO DE LA REGIÓN LORETO - PLAZO DETERMINADO (009291)', p)
        self.assertEqual(c, 'Docente de inglés (Colegio de Alto Rendimiento de la región Loreto)')
        c = normalizar.cargo_final('CONTRATAR LOS SERVICIOS DE UN/A (01) PROMOTOR/A PARA EL CENTRO DE EMERGENCIA MUJER Y FAMILIA REGULAR POMALCA – LAMBAYEQUE', p)
        self.assertEqual(c, 'Promotor/a del Centro Emergencia Mujer (CEM)')

    def test_fecha_y_ubicacion(self):
        self.assertEqual(normalizar.fecha_iso('21/10/2026'), '2026-10-21')
        self.assertEqual(normalizar.fecha_iso('7/1/2027'), '2027-01-07')
        self.assertIsNone(normalizar.fecha_iso('mañana'))
        self.assertEqual(normalizar.departamento_desde_ubicacion('MADRE DE DIOS - TAMBOPATA'), ('Madre de Dios', 'TAMBOPATA'))
        self.assertEqual(normalizar.departamento_desde_ubicacion('ANCASH - HUARI')[0], 'Áncash')


class TestSERVIR(unittest.TestCase):
    OFERTA = ('<div class="cuadro-vacantes"><div class="titulo-vacante"><label>CONTADOR</label></div><div class="nombre-entidad">ENTIDAD X</div>'
              '<span class="sub-titulo">Ubicación:</span><span class="detalle-sp">AREQUIPA - CAYMA</span>'
              '<span class="sub-titulo">Número de Convocatoria:</span><span class="detalle-sp">728-02</span>'
              '<span class="sub-titulo">Cantidad de Vacantes:</span><span class="detalle-sp">2</span>'
              '<span class="sub-titulo">Remuneración:</span><span class="detalle-sp">S/. 6,300.00</span>'
              '<span class="sub-titulo">Fecha Fin de Publicación:</span><span class="detalle-sp">21/10/2026</span></div>')
    PRACTICA = ('<div class="col-sm-12 cuadro-vacantes"><div class="col-sm-12 titulo-vacante"><label>PRACTICANTE PROFESIONAL</label></div>'
                '<div class="nombre-entidad"> OEFA </div><div class="col-sm-3 sub-titulo"> Tipo de Modalidad: </div><div class="col-sm-9 detalle-sp"> Practicas Profesionales </div>'
                '<div class="col-sm-6 sub-titulo">Ubicación:</div> <div class="col-sm-6 detalle-sp"> MADRE DE DIOS - TAMBOPATA</div>'
                '<div class="col-sm-6 sub-titulo">Número de Convocatoria:</div> <div class="col-sm-6 detalle-sp"> 077 - 2026</div>'
                '<div class="col-sm-6 sub-titulo">Número de Vacante:</div> <div class="col-sm-6 detalle-sp"> 1</div>'
                '<div class="col-sm-6 sub-titulo">Cierre de Publicación:</div> <div class="col-sm-6 detalle-sp">07/10/2026 </div></div>')

    def test_lee_oferta_laboral(self):
        o = servir.leer_bloques(self.OFERTA)[0]
        self.assertEqual((o['cargo'], o['entidad'], o['numero'], o['vacantes'], o['remuneracion'], o['fin']),
                         ('CONTADOR', 'ENTIDAD X', '728-02', '2', 'S/. 6,300.00', '21/10/2026'))

    def test_etiquetas_partidas_en_dos_lineas(self):
        # así llega de verdad desde el portal: la etiqueta con saltos de línea y tabulaciones
        t = ('<div class="cuadro-vacantes"><div class="titulo-vacante"><label>PRACTICANTE PROFESIONAL</label></div><div class="nombre-entidad"> OEFA </div>'
             '<div class="row box-mb cuadro-detalle">\n\t\t<div class="col-sm-6 sub-titulo">Número de\n\t\t\tConvocatoria:</div>\n\t\t<div class="col-sm-6 detalle-sp">\n\t\t\t077 - 2026</div></div>'
             '<div class="row"><div class="col-sm-6 sub-titulo">Cierre de\n\t\t\tPublicación:</div>\n\t\t<div class="col-sm-6 detalle-sp">07/10/2026\n\t\t</div></div></div>')
        o = servir.leer_bloques(t)[0]
        self.assertEqual((o['numero'], o['fin']), ('077 - 2026', '07/10/2026'))

    def test_lee_practica(self):
        o = servir.leer_bloques(self.PRACTICA)[0]
        self.assertEqual((o['cargo'], o['modalidad'], o['ubicacion'], o['numero'], o['fin']),
                         ('PRACTICANTE PROFESIONAL', 'Practicas Profesionales', 'MADRE DE DIOS - TAMBOPATA', '077 - 2026', '07/10/2026'))


class TestSeleccion(unittest.TestCase):
    def test_oferta_buena_pasa(self):
        r = rec()
        self.assertIsNone(seleccion.motivo_descarte(r, CFG, HOY))
        self.assertEqual((r['tipo'], r['sueldo'], r['cierre'], r['region']), ('CAS', 3500.0, '2026-10-21', 'Cusco'))

    def test_descartes(self):
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='PERSONAL DE LIMPIEZA'), CFG, HOY), 'labor manual')
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='VILANTE'), CFG, HOY), 'labor manual')
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='.'), CFG, HOY), 'cargo basura')
        self.assertEqual(seleccion.motivo_descarte(rec(sueldo='S/. 002.16'), CFG, HOY), 'sueldo fuera de rango')
        self.assertEqual(seleccion.motivo_descarte(rec(sueldo='S/. 936,419.00'), CFG, HOY), 'sueldo fuera de rango')
        self.assertEqual(seleccion.motivo_descarte(rec(numero='276-001'), CFG, HOY), 'régimen no CAS ni 728')
        self.assertEqual(seleccion.motivo_descarte(rec(fin=''), CFG, HOY), 'sin fecha de cierre')
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='HOSPITAL DE APOYO HUARMEY'), CFG, HOY), 'cargo cortado o con error')

    def test_fechas_respetan_dias_minimos(self):
        self.assertIsNone(seleccion.motivo_descarte(rec(fin='10/10/2026'), CFG, HOY))        # 3 días: justo
        self.assertIsNotNone(seleccion.motivo_descarte(rec(fin='09/10/2026'), CFG, HOY))      # 2 días: poco
        self.assertIsNotNone(seleccion.motivo_descarte(rec(fin='05/10/2026'), CFG, HOY))      # ya cerró

    def test_practicas_no_piden_sueldo_ni_regimen(self):
        o = {'cargo': 'PRACTICANTE PRE PROFESIONAL', 'entidad': 'OEFA', 'ubicacion': 'MADRE DE DIOS - TAMBOPATA', 'numero': '077 - 2026', 'vacantes': '1',
             'remuneracion': '', 'fin': '20/10/2026', 'inicio': '', 'modalidad': 'Practicas Pre Profesionales'}
        r = seleccion.convertir(o, 'servir-practicas')
        self.assertEqual(r['region'], 'Madre de Dios')
        self.assertIsNone(seleccion.motivo_descarte(r, CFG, HOY))
        d = seleccion.documento(r, 'ce-x-1')
        self.assertEqual(d['tipo'], 'Prácticas')
        self.assertNotIn('sueldo', d)
        self.assertIn('Prácticas', d['descripcion'])

    def test_elegir_tope_por_region_y_entidad_e_indeterminado_primero(self):
        recs = [rec(cargo=f'ANALISTA {i}', entidad=f'ENTIDAD {i % 8}', numero=CAS + f'-{i}', fin=f'{20 - (i % 5):02d}/10/2026') for i in range(1, 31)]
        recs.append(rec(cargo='ESPECIALISTA INDET', entidad='ENTIDAD 99', numero='D.LEG 1057 - INDETERMINADO-1', fin='12/10/2026'))
        elegidas, sobrantes = seleccion.elegir(recs, CFG)
        self.assertEqual(len(elegidas), 10)
        self.assertEqual(len(elegidas) + len(sobrantes), len(recs))
        self.assertIn('ESPECIALISTA INDET', [r['cargo_raw'] for r in elegidas])  # el contrato indeterminado entra aunque cierre antes
        por_entidad = {}
        for r in elegidas:
            por_entidad[r['institucion']] = por_entidad.get(r['institucion'], 0) + 1
        self.assertTrue(all(n <= 2 for n in por_entidad.values()))
        self.assertEqual([r['cierre'] for r in elegidas], sorted((r['cierre'] for r in elegidas), reverse=True))

    def test_sin_repetidas_es_estable(self):
        a = rec(numero=CAS + '-1')
        b = rec(numero=CAS + '-2')  # mismo cargo, entidad, lugar y cierre
        self.assertEqual(len(seleccion.sin_repetidas([a, b])), 1)
        self.assertEqual(seleccion.sin_repetidas([a, b])[0]['clave_base'], seleccion.sin_repetidas([b, a])[0]['clave_base'])

    def test_documento_para_uninexo(self):
        r = rec()
        d = seleccion.documento(r, 'ce-cusco-20261007-01')
        self.assertEqual((d['departamento'], d['tipo'], d['sueldo'], d['sueldoNumero'], d['fechaCierre'], d['estado']),
                         ('Cusco', 'CAS', 'S/. 3,500.00', 3500.0, '2026-10-21', 'disponible'))
        self.assertIn('En SERVIR elige Ubicación CUSCO y busca la de Municipalidad Distrital de San Pablo, número de convocatoria: ' + CAS + '-8.', d['descripcion'])
        self.assertTrue(d['enlaceOficial'].startswith('https://app.servir.gob.pe/'))
        self.assertEqual(seleccion.ids_para([r, r], HOY), ['ce-cusco-20261007-01', 'ce-cusco-20261007-02'])


class TestGobPe(unittest.TestCase):
    def test_fechas_en_espanol(self):
        self.assertEqual(gobpe.fecha_desde_texto(' 7 de octubre de 2026'), '2026-10-07')
        self.assertEqual(gobpe.fecha_desde_texto('14 de setiembre de 2026'), '2026-09-14')
        self.assertIsNone(gobpe.fecha_desde_texto('sin fecha'))

    def test_filtro_de_titulos(self):
        self.assertTrue(gobpe.es_convocatoria('Proceso CAS N° 017-2026- Digitador- SUNARP-ZRN°XI'))
        self.assertTrue(gobpe.es_convocatoria('Convocatoria Practicas N° 064-2026 PRACTICANTE PROFESIONAL'))
        self.assertTrue(gobpe.es_convocatoria('Concurso Público de Méritos N°01-2026-SUNARP/ZRXII'))
        self.assertFalse(gobpe.es_convocatoria('Contratos Menores N° 020-2026-OC-OEFA'))
        self.assertFalse(gobpe.es_convocatoria('Resultados de evaluación curricular - Convocatoria CAS 034'))
        self.assertFalse(gobpe.es_convocatoria('Requerimiento para la contratación de Locación de Servicios'))
        self.assertFalse(gobpe.es_convocatoria('Acta de sesiones año 2026'))

    def test_lee_tarjetas_del_listado(self):
        t = ('<ul><li class="x"><div><a class="mb-2 card__mock mr-10" href="/institucion/sunarp/informes-publicaciones/8680564-concurso-interno">Concurso Interno de Méritos 001-2026</a>'
             '<time datetime="2026-10-05 09:14:00.000"> 5 de octubre de 2026</time></div></li>'
             '<li><a class="otra" href="/institucion/sunarp/informes-publicaciones/tipos/80-convocatoria">Tipos</a></li></ul>')
        r = gobpe.leer_tarjetas(t, 'sunarp')
        self.assertEqual(len(r), 1)
        self.assertEqual((r[0]['fecha'], r[0]['slug'], r[0]['institucion']), ('2026-10-05', 'sunarp', 'SUNARP'))
        self.assertEqual(r[0]['url'], 'https://www.gob.pe/institucion/sunarp/informes-publicaciones/8680564-concurso-interno')


class TestAlmacen(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.alm = almacen.Almacen(os.path.join(self.dir, 'e.sqlite'))

    def tearDown(self):
        self.alm.cerrar()

    def test_ofertas_vistas_y_ampliadas(self):
        self.assertTrue(self.alm.es_primera_vez())
        self.assertIsNone(self.alm.cierre_guardado('k'))
        self.alm.guardar_oferta('k', 'servir-ofertas', 'Cusco', 'Contador', '2026-10-21', '2026-10-07')
        self.assertEqual(self.alm.cierre_guardado('k'), '2026-10-21')
        self.alm.guardar_oferta('k', 'servir-ofertas', 'Cusco', 'Contador', '2026-10-28', '2026-10-10')  # ampliada
        self.assertEqual(self.alm.cierre_guardado('k'), '2026-10-28')
        self.assertEqual(self.alm.contar_ofertas(), 1)
        self.alm.poner_meta('base_inicial', '2026-10-07')
        self.assertFalse(self.alm.es_primera_vez())

    def test_enlaces_y_paginas(self):
        self.assertFalse(self.alm.enlace_visto('u'))
        self.alm.guardar_enlace('u', 'f', 't', '2026-10-07', '2026-10-07')
        self.alm.guardar_enlace('u', 'f', 't', '2026-10-07', '2026-10-08')
        self.assertTrue(self.alm.enlace_visto('u'))
        self.assertEqual(self.alm.contar_enlaces(), 1)
        self.assertIsNone(self.alm.pagina('p'))
        self.alm.guardar_pagina('p', ['a', 'b'], '2026-10-07')
        self.assertEqual(self.alm.pagina('p')['lineas'], ['a', 'b'])
        self.alm.marcar_error_pagina('p', '2026-10-08')
        self.assertTrue(self.alm.pagina('p')['error_avisado'])
        self.alm.guardar_pagina('p', ['a'], '2026-10-09')
        self.assertFalse(self.alm.pagina('p')['error_avisado'])


class TestVigilante(unittest.TestCase):
    def test_texto_visible(self):
        l = vigilante.lineas_de_html('<html><head><title>x</title><script>var a=1;</script></head><body><div>Convocatoria CAS N° 001-2026 abierta hasta el 20</div>'
                                     '<p>corto</p><style>.a{}</style><li>Proceso de selección de practicantes 2026 inscripciones abiertas</li></body></html>')
        self.assertEqual(l, ['Convocatoria CAS N° 001-2026 abierta hasta el 20', 'Proceso de selección de practicantes 2026 inscripciones abiertas'])

    def test_avisa_solo_lo_nuevo(self):
        class Falso:
            def __init__(s):
                s.d = {}

            def pagina(s, i):
                return s.d.get(i)

            def guardar_pagina(s, i, lineas, hoy, error_avisado=0):
                s.d[i] = {'lineas': lineas, 'ultima': hoy, 'error_avisado': False}

            def marcar_error_pagina(s, i, hoy):
                s.d[i] = {'lineas': [], 'ultima': hoy, 'error_avisado': True}
        alm, textos = Falso(), ['<div>Convocatoria vieja número uno publicada</div>']
        original = vigilante._descargar
        vigilante._descargar = lambda url: '<body>' + ''.join(textos) + '</body>'
        try:
            f = {'id': 'x', 'nombre': 'X', 'url': 'http://x', 'modo': 'texto'}
            r1 = vigilante.revisar(f, alm, '2026-10-07')
            self.assertTrue(r1['primera'])
            self.assertEqual(r1['cambios'], [])
            textos.append('<div>Nueva convocatoria CAS número dos ya disponible</div><div>Noticia del clima de hoy en la ciudad</div>')
            r2 = vigilante.revisar(f, alm, '2026-10-08')
            self.assertEqual(r2['cambios'], ['Nueva convocatoria CAS número dos ya disponible'])
            self.assertEqual(vigilante.revisar(f, alm, '2026-10-09')['cambios'], [])
        finally:
            vigilante._descargar = original


class TestTelegramYMensajes(unittest.TestCase):
    def test_partir_respeta_limite(self):
        bloques = [f'bloque {i} ' + 'x' * 900 for i in range(10)]
        ms = telegram.partir(bloques, 3800)
        self.assertTrue(all(len(m) <= 3800 for m in ms))
        self.assertEqual(''.join(ms).count('bloque'), 10)
        self.assertEqual(telegram.partir(['a' * 9000], 3800)[0], 'a' * 3800)

    def test_escapa_html(self):
        self.assertEqual(telegram.esc('A & B <c>'), 'A &amp; B &lt;c&gt;')

    def test_linea_de_oferta(self):
        r = rec(numero='D.LEG 1057 - INDETERMINADO-032', fin='21/10/2026')
        t = mensajes.linea_oferta(r, HOY)
        self.assertIn('<b>Especialista en contabilidad</b>', t)
        self.assertIn('S/ 3,500', t)
        self.assertIn('cierra 21/10 (14 días)', t)
        self.assertIn('CAS indeterminado N.º 032', t)
        self.assertIn('AMPLIADA', mensajes.linea_oferta(r, HOY, ampliada=True))

    def test_resumen_sin_novedades_y_con_errores(self):
        self.assertIn('no hay novedades', mensajes.mensaje_resumen(HOY, 0, 0, 0, 0, [], 20))
        t = mensajes.mensaje_resumen(HOY, 3, 0, 1, 0, ['SERVIR Piura: tiempo agotado'], 20)
        self.assertIn('Plazas nuevas: 3', t)
        self.assertIn('SERVIR Piura', t)

    def test_env(self):
        d = tempfile.mkdtemp()
        ruta = os.path.join(d, '.env')
        with open(ruta, 'w', encoding='utf-8') as fh:
            fh.write('# nota\nTELEGRAM_BOT_TOKEN="abc:123"\nTELEGRAM_CHAT_ID=42\n')
        self.assertEqual(telegram.cargar_env(ruta), {'TELEGRAM_BOT_TOKEN': 'abc:123', 'TELEGRAM_CHAT_ID': '42'})
        with self.assertRaises(telegram.ErrorTelegram):
            telegram.Telegram('', '')


def cfg_con(**reglas_):
    c = json.loads(json.dumps(CFG))
    c['reglas'] = {'regiones': {}, 'carreras': {}, 'cargos': {}}
    for k, v in reglas_.items():
        c['reglas'][k] = v
    return c


class TestReglasRegionYCarrera(unittest.TestCase):
    def test_reconoce_carreras_por_el_cargo(self):
        import reglas
        self.assertEqual(reglas.carreras_de('Abogado registral')[:1], ['Derecho'])
        self.assertIn('Contabilidad', reglas.carreras_de('Analista contable en presupuesto'))
        self.assertIn('Enfermería', reglas.carreras_de('Técnico/a en enfermería'))
        self.assertIn('Ing. de Sistemas', reglas.carreras_de('Ingeniero de sistemas'))
        self.assertIn('Educación', reglas.carreras_de('Docente de inglés (Colegio de Alto Rendimiento)'))
        self.assertIn('Odontología', reglas.carreras_de('Cirujano dentista'))
        self.assertNotIn('Medicina', reglas.carreras_de('Cirujano dentista'))
        self.assertEqual(reglas.carreras_de('Especialista III'), [])

    def test_sin_reglas_todo_pasa_y_solo_se_etiqueta(self):
        r = rec(cargo='ABOGADO')
        self.assertIn('Derecho', r['carreras'])
        self.assertIsNone(seleccion.motivo_descarte(r, cfg_con(), HOY))

    def test_solo_ciertas_carreras(self):
        c = cfg_con(carreras={'solo': ['Derecho', 'Contabilidad'], 'incluir_sin_carrera': True})
        self.assertIsNone(seleccion.motivo_descarte(rec(cargo='ABOGADO'), c, HOY))
        self.assertIsNone(seleccion.motivo_descarte(rec(cargo='CONTADOR'), c, HOY))
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='ENFERMERO/A'), c, HOY), 'otra carrera (no está en tu lista)')
        self.assertIsNone(seleccion.motivo_descarte(rec(cargo='ESPECIALISTA III'), c, HOY))  # sin carrera clara: pasa
        c['reglas']['carreras']['incluir_sin_carrera'] = False
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='ESPECIALISTA III'), c, HOY), 'sin carrera reconocida')

    def test_carreras_ignoradas_y_palabras(self):
        c = cfg_con(carreras={'ignorar': ['Enfermería']})
        self.assertEqual(seleccion.motivo_descarte(rec(cargo='ENFERMERO/A'), c, HOY), 'carrera ignorada por tu regla')
        self.assertIsNone(seleccion.motivo_descarte(rec(cargo='ABOGADO'), c, HOY))
        c = cfg_con(cargos={'excluir_palabras': ['secretaria']})
        self.assertIn('excluido', seleccion.motivo_descarte(rec(cargo='SECRETARIA I'), c, HOY))
        c = cfg_con(carreras={'solo': ['Derecho']}, cargos={'incluir_palabras': ['contador']})
        self.assertIsNone(seleccion.motivo_descarte(rec(cargo='CONTADOR'), c, HOY))  # «siempre incluir» gana

    def test_regiones_solo_ignorar_prioridad_y_tope(self):
        import reglas
        c = cfg_con(regiones={'solo': ['Cusco', 'Madre de Dios'], 'prioritarias': ['Madre de Dios'], 'tope_propio': {'Madre de Dios': 15}})
        self.assertTrue(reglas.region_permitida('Cusco', c))
        self.assertFalse(reglas.region_permitida('Lima', c))
        self.assertEqual(seleccion.motivo_descarte(rec(), cfg_con(regiones={'ignorar': ['Cusco']}), HOY), 'región fuera de tu lista')
        self.assertEqual(reglas.orden_regiones(['Cusco', 'Madre de Dios', 'Arequipa'], cfg_con(regiones={'prioritarias': ['Madre de Dios']})),
                         ['Madre de Dios', 'Arequipa', 'Cusco'])
        self.assertEqual(reglas.tope_region('Madre de Dios', c), 15)
        self.assertEqual(reglas.tope_region('Cusco', c), 10)

    def test_tope_propio_en_la_eleccion(self):
        c = cfg_con(regiones={'tope_propio': {'Cusco': 3}})
        recs = [rec(cargo=f'ANALISTA {i}', entidad=f'ENTIDAD {i}', numero=CAS + f'-{i}') for i in range(1, 9)]
        self.assertEqual(len(seleccion.elegir(recs, c)[0]), 3)

    def test_mensaje_con_prioridad_y_carrera_y_documento(self):
        c = cfg_con(regiones={'prioritarias': ['Madre de Dios']})
        a = seleccion.convertir(cruda(cargo='ABOGADO', ubic='MADRE DE DIOS - TAMBOPATA'), 'servir-ofertas', 'Madre de Dios')
        b = rec(cargo='CONTADOR')
        bl = mensajes.bloques_plazas('Nuevas', {'Cusco': [b], 'Madre de Dios': [a]}, HOY, (), c)
        self.assertIn('⭐ <b>Madre de Dios</b>', bl[1])
        self.assertIn('Cusco', bl[2])
        self.assertIn('🎓 Derecho', bl[1])
        self.assertEqual(seleccion.documento(b, 'ce-x')['carrera'], 'Contabilidad')


class TestInforme(unittest.TestCase):
    def datos(self):
        a = rec(cargo='ABOGADO <script>', entidad='ENTIDAD & CIA')
        return {'Cusco': [a]}

    def test_html_del_informe(self):
        import informe
        c = cfg_con(regiones={'prioritarias': ['Cusco']}, carreras={'solo': ['Derecho']})
        h = informe.construir_html(HOY, self.datos(), {}, [{'titulo': 'Proceso CAS N° 1', 'url': 'https://x.pe/a?b=1&c=2', 'fecha': '2026-10-07', 'institucion': 'SUNARP', 'slug': 's', 'fuente': 'g'}],
                                   [], ['SERVIR Piura: tiempo agotado'], c, set())
        self.assertIn('Informe del miércoles 7 de octubre de 2026', h)
        self.assertIn('⭐ Cusco', h)
        self.assertIn('Abogado &lt;script&gt;', h)          # nada de HTML inyectado desde el portal
        self.assertNotIn('<script>', h.split('</style>')[1])
        self.assertIn('Entidad &amp; Cia', h)                # el & también se escapa
        self.assertIn('1 plaza nueva', h)
        self.assertIn('1 anuncio en gob.pe', h)
        self.assertIn('0 páginas con cambios', h)
        self.assertIn('href="https://x.pe/a?b=1&amp;c=2"', h)
        self.assertIn('Carreras: Derecho', h)
        self.assertIn('SERVIR Piura', h)

    def test_crea_un_pdf_de_verdad(self):
        import informe
        try:
            informe.buscar_navegador()
        except informe.ErrorInforme:
            self.skipTest('no hay Edge ni Chrome en esta PC')
        ruta = os.path.join(tempfile.mkdtemp(), 'prueba.pdf')
        informe.html_a_pdf(informe.construir_html(HOY, self.datos(), {}, [], [], [], CFG, set()), ruta)
        with open(ruta, 'rb') as f:
            datos = f.read()
        self.assertTrue(datos.startswith(b'%PDF'))
        self.assertGreater(len(datos), 5000)


class TestPublicado(unittest.TestCase):
    def test_reconoce_lo_ya_publicado(self):
        r = rec()
        claves = publicado.claves_de(r['numero'], r['cierre'], r['cargo'], r['institucion'])
        self.assertTrue(publicado.ya_publicada(r, claves))
        otra = rec(cargo='ANALISTA LEGAL')
        self.assertFalse(publicado.ya_publicada(otra, claves))


if __name__ == '__main__':
    unittest.main()
