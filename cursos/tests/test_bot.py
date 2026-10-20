"""Pruebas del bot de Cursos (sin internet). Correr con:  python -m unittest discover -s tests -v   (desde D:\\uninexo-bot-cursos)"""
import json
import os
import sys
import tempfile
import unittest
from datetime import date
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import clasificar  # noqa: E402
import gobpe  # noqa: E402
import informe  # noqa: E402
import mensajes  # noqa: E402
import publicado  # noqa: E402
import reglas  # noqa: E402
import seleccion  # noqa: E402
import telegram  # noqa: E402

HOY = date(2026, 10, 7)
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json'), encoding='utf-8') as _f:
    CFG = json.load(_f)

# Los campos que acepta la cola de revisión de la app (firestore.rules → isValidCursoPendiente)
CAMPOS_PERMITIDOS = {'name', 'career', 'region', 'university', 'description', 'whatsappUrl', 'enlaceOficial', 'tipo', 'modalidad', 'institucion', 'gratuito', 'costoTexto',
                     'certificado', 'area', 'fechaLimite', 'nivel'}


def cfg_con(**reglas_):
    c = json.loads(json.dumps(CFG))
    c['reglas'] = {'tipos': {}, 'areas': {}, 'instituciones': {}}
    c['reglas'].update(reglas_)
    return c


def item(titulo='Curso virtual: Producción de cuyes', slug='inia', fecha='2026-10-06', fuente='gobpe-campañas'):
    return {'titulo': titulo, 'url': f'https://www.gob.pe/institucion/{slug}/campa%C3%B1as/123-x', 'fecha': fecha, 'slug': slug, 'fuente': fuente}


def cand(titulo='Curso virtual: Producción de cuyes', slug='inia', **extra):
    c = seleccion.candidato_desde(item(titulo, slug), HOY, leer_pagina=False)
    c.update(extra)
    return c


class TestClasificar(unittest.TestCase):
    def test_tipo_por_el_titulo(self):
        casos = {
            'Beca Generación del Bicentenario - Convocatoria 2026': 'beca',
            'Programa de Extensión Universitaria - PEU OSIPTEL': 'especializacion',
            'Diplomado en Tecnologías de la Información': 'diplomado',
            'Curso Online Gratuito de Quechua Central': 'curso',
            'Taller de oratoria para jóvenes': 'taller',
            'Webinar Osinergmin': 'webinar',
            'Ciberseminarios en Voluntariado 2026': 'voluntariado',
            'Concurso de Ensayos para jóvenes sobre ciencia': 'convocatoria',
        }
        for titulo, tipo in casos.items():
            self.assertEqual(clasificar.tipo_de(titulo), tipo, titulo)

    def test_no_es_oportunidad_lo_que_es_empleo_resultado_o_ruido(self):
        for titulo in ['Convocatoria CAS N° 012-2026 Asistente administrativo', 'Resultados del concurso de becas', 'Lista de admitidos al curso de gestión',
                       'Oficio múltiple sobre el diplomado de directivos', 'Ceremonia de clausura del curso de oratoria', 'Concurso Nacional del Pisco 2026',
                       'Accede al servicio de Acceso a la Información Pública', 'Convocatoria de prácticas pre profesionales 2026']:
            self.assertFalse(clasificar.es_oportunidad(titulo, HOY), titulo)
        self.assertTrue(clasificar.es_oportunidad('Curso virtual: Manejo Integrado de Cultivos Tropicales', HOY))

    def test_una_fecha_vencida_en_el_titulo_es_un_evento_que_ya_paso(self):
        self.assertFalse(clasificar.es_oportunidad('Capacitación Virtual 28/08/2026', HOY))
        self.assertTrue(clasificar.es_oportunidad('Capacitación Virtual 28/10/2026', HOY))

    def test_area_y_region(self):
        self.assertEqual(clasificar.area_de('Curso de inglés básico'), 'Idiomas')
        self.assertEqual(clasificar.area_de('Diplomado en derecho constitucional'), 'Derecho y Ciencias Políticas')
        self.assertEqual(clasificar.area_de('Taller de bienvenida'), clasificar.AREA_TODAS)
        self.assertEqual(clasificar.region_de('Curso de turismo en Madre de Dios'), 'Madre de Dios')
        self.assertEqual(clasificar.region_de('Curso nacional de turismo'), 'Todo el país')

    def test_pagina_dice_gratis_fecha_limite_y_modalidad(self):
        t = ('<html><head><meta property="og:description" content="Curso virtual y gratuito de quechua para todo el país, con certificado al finalizar."></head>'
             '<body><p>Las inscripciones están abiertas hasta el 25 de noviembre de 2026.</p><p>El curso es 100% virtual.</p></body></html>')
        d = clasificar.analizar_pagina(t, HOY)
        self.assertTrue(d['gratuito'])
        self.assertEqual(d['fechaLimite'], '2026-11-25')
        self.assertEqual(d['modalidad'], 'virtual')
        self.assertIn('quechua', d['descripcion'])

    def test_pagina_con_costo_o_sin_datos_no_inventa(self):
        d = clasificar.analizar_pagina('<body><p>Inversión: S/ 350 por participante. Inscripciones hasta el 12/10/2026. Modalidad presencial.</p></body>', HOY)
        self.assertEqual((d['gratuito'], d['costo'], d['fechaLimite'], d['modalidad']), (False, 'S/ 350', '2026-10-12', 'presencial'))
        vacia = clasificar.analizar_pagina('<body><p>Bienvenidos a nuestra institución.</p></body>', HOY)
        self.assertNotIn('gratuito', vacia)
        self.assertNotIn('fechaLimite', vacia)

    def test_fechas_lejanas_o_pasadas_no_son_fecha_limite(self):
        self.assertEqual(clasificar.fechas_clave('Inscripciones hasta el 01/09/2026 y clases hasta el 15 de agosto de 2027.', HOY), [])


class TestReglas(unittest.TestCase):
    def test_sin_reglas_pasa_lo_nacional(self):
        self.assertIsNone(reglas.evaluar(cand(), cfg_con(), HOY))

    def test_instituciones_locales_se_ignoran_salvo_las_que_pides(self):
        self.assertEqual(reglas.evaluar(cand(slug='muniarequipa'), cfg_con(), HOY), 'institución local o ignorada')
        self.assertEqual(reglas.evaluar(cand(slug='ugeltacna'), cfg_con(), HOY), 'institución local o ignorada')
        self.assertIsNone(reglas.evaluar(cand(slug='unamad'), cfg_con(instituciones={'incluir': ['unamad']}), HOY))
        self.assertIsNone(reglas.evaluar(cand(slug='muniarequipa'), cfg_con(incluir_locales=True), HOY))
        self.assertEqual(reglas.evaluar(cand(), cfg_con(instituciones={'ignorar': ['inia']}), HOY), 'institución local o ignorada')

    def test_tipos_y_areas(self):
        c = cand('Beca de maestría en derecho', 'pronabec')
        self.assertIsNone(reglas.evaluar(c, cfg_con(tipos={'solo': ['beca']}), HOY))
        self.assertEqual(reglas.evaluar(c, cfg_con(tipos={'solo': ['curso']}), HOY), 'otro tipo (no está en tu lista)')
        self.assertEqual(reglas.evaluar(c, cfg_con(tipos={'ignorar': ['beca']}), HOY), 'tipo ignorado por tu regla')
        self.assertIsNone(reglas.evaluar(c, cfg_con(areas={'solo': ['Derecho y Ciencias Políticas']}), HOY))
        self.assertEqual(reglas.evaluar(c, cfg_con(areas={'solo': ['Salud']}), HOY), 'otra área (no está en tu lista)')
        self.assertIsNone(reglas.evaluar(cand('Taller de bienvenida'), cfg_con(areas={'solo': ['Salud']}), HOY))  # sin área clara: pasa

    def test_solo_gratuitos(self):
        c = cand()
        base = {'solo_gratuitos': True}
        self.assertEqual(reglas.evaluar({**c, 'gratuito': False}, cfg_con(**base), HOY), 'de pago')
        self.assertIsNone(reglas.evaluar({**c, 'gratuito': True}, cfg_con(**base), HOY))
        self.assertIsNone(reglas.evaluar({**c, 'gratuito': None}, cfg_con(**base), HOY))
        self.assertEqual(reglas.evaluar({**c, 'gratuito': None}, cfg_con(solo_gratuitos=True, incluir_costo_desconocido=False), HOY), 'no dice si es gratis')

    def test_fecha_limite_con_margen(self):
        c = cand()
        self.assertIsNone(reglas.evaluar({**c, 'fechaLimite': '2026-10-09'}, cfg_con(dias_minimos_abierta=2), HOY))
        self.assertEqual(reglas.evaluar({**c, 'fechaLimite': '2026-10-08'}, cfg_con(dias_minimos_abierta=2), HOY), 'cierra muy pronto o ya cerró')
        self.assertEqual(reglas.evaluar({**c, 'fechaLimite': '2026-10-01'}, cfg_con(), HOY), 'cierra muy pronto o ya cerró')

    def test_palabras_excluidas(self):
        self.assertIn('excluido', reglas.evaluar(cand('Curso de oratoria básica'), cfg_con(palabras_excluir=['oratoria']), HOY))


class TestSeleccionYDocumento(unittest.TestCase):
    def test_url_canonica_ignora_www_barra_final_y_mayusculas(self):
        a = seleccion.url_canonica('https://www.gob.pe/institucion/INIA/campa%C3%B1as/12-Curso/')
        b = seleccion.url_canonica('http://gob.pe/institucion/inia/campañas/12-curso')
        self.assertEqual(a, b)

    def test_documento_solo_con_campos_que_acepta_la_cola_de_revision(self):
        c = cand('Curso Online Gratuito de Quechua Central', 'cultura', gratuito=True, fechaLimite='2026-11-25', modalidad='virtual', descripcion='Curso virtual de quechua.')
        d = seleccion.documento(c, HOY)
        self.assertTrue(set(d) <= CAMPOS_PERMITIDOS, set(d) - CAMPOS_PERMITIDOS)
        self.assertEqual((d['tipo'], d['gratuito'], d['fechaLimite'], d['modalidad'], d['area'], d['career']), ('curso', True, '2026-11-25', 'virtual', 'Idiomas', 'Idiomas'))
        self.assertNotIn('costoTexto', d)
        self.assertTrue(d['enlaceOficial'].startswith('https://'))
        self.assertLessEqual(len(d['name']), 150)
        self.assertLessEqual(len(d['description']), 1000)
        self.assertIn('Revisa las bases', d['description'])

    def test_si_no_se_sabe_el_costo_va_por_confirmar_nunca_gratis(self):
        d = seleccion.documento(cand(gratuito=None), HOY)
        self.assertEqual((d['gratuito'], d['costoTexto']), (False, 'Por confirmar'))
        d = seleccion.documento(cand(gratuito=False, costo='S/ 350'), HOY)
        self.assertEqual((d['gratuito'], d['costoTexto']), (False, 'S/ 350'))

    def test_orden_becas_primero_y_luego_lo_que_cierra_antes(self):
        a, b, c = cand('Taller de oratoria', fechaLimite=None), cand('Beca de maestría', 'pronabec'), cand('Curso de excel', fechaLimite='2026-10-20')
        self.assertEqual([x['tipo'] for x in sorted([a, b, c], key=seleccion.prioridad)], ['beca', 'curso', 'taller'])

    def test_lectura_de_la_lista_de_campanas(self):
        t = ('<ul><li><a href="/institucion/inia/campa%C3%B1as/145-curso-virtual-cuyes">Curso virtual: Producción de cuyes</a><time datetime="2026-07-01 08:00:00.000"> 1 de julio de 2026</time></li>'
             '<li><a href="/institucion/inia/informes-publicaciones/9-otro">Otro</a></li></ul>')
        r = gobpe.leer_tarjetas_campanas(t, 'inia')
        self.assertEqual(len(r), 1)
        self.assertEqual((r[0]['titulo'], r[0]['fecha'], r[0]['slug']), ('Curso virtual: Producción de cuyes', '2026-07-01', 'inia'))

    def test_la_busqueda_ignora_un_resultado_null_de_gobpe(self):
        # pasó el 08/10/2026 con «especialización»: gob.pe mandó null en medio de la lista y la búsqueda entera fallaba
        bueno = {'url': '<a href="/institucion/inia/campa%C3%B1as/145-curso-virtual-cuyes">Curso virtual: Producción de cuyes</a>', 'publication': 'Publicado el 1 de julio de 2026'}
        cuerpo = json.dumps({'data': {'attributes': {'results': [None, bueno, None]}}})
        with mock.patch.object(gobpe, 'descargar', return_value=cuerpo):
            r = gobpe.buscar('especialización', 'campañas', pausa=0)
        self.assertEqual([x['fecha'] for x in r], ['2026-07-01'])


class TestPublicado(unittest.TestCase):
    PUB = {'urls': {'beca.osiptel.gob.pe'}, 'cursos': [('OSIPTEL, Programa de Extensión Universitaria: 60 becas integrales en regulación', 'OSIPTEL')]}

    def test_reconoce_lo_ya_publicado_por_enlace_o_por_nombre(self):
        mismo_enlace = cand('Beca X', 'osiptel')
        mismo_enlace['enlaceOficial'] = 'https://www.beca.osiptel.gob.pe/'
        self.assertTrue(publicado.ya_publicada(mismo_enlace, self.PUB))
        self.assertTrue(publicado.ya_publicada(cand('Programa de Extensión Universitaria - PEU OSIPTEL becas', 'osiptel'), self.PUB))
        self.assertFalse(publicado.ya_publicada(cand('Curso virtual de cuyes', 'inia'), self.PUB))


class TestMensajesEInforme(unittest.TestCase):
    def datos(self):
        return [cand('Curso Online Gratuito de Quechua <b>Central</b>', 'cultura', gratuito=True, fechaLimite='2026-10-10', modalidad='virtual'), cand('Beca de maestría', 'pronabec')]

    def test_mensajes_con_el_distintivo_de_cursos(self):
        t = mensajes.mensaje_resumen(HOY, 2, 1, 0, [], 20, con_pdf=True)
        self.assertTrue(t.startswith('📚'))
        self.assertIn('detalle va en el PDF', t)
        self.assertTrue(mensajes.mensaje_resumen(HOY, 0, 0, 0, [], 20).startswith('📚'))
        self.assertTrue(mensajes.mensaje_inicial(100, 10).startswith('📚'))
        texto = '\n'.join(mensajes.bloques_candidatos(self.datos(), HOY))
        self.assertIn('Gratis', texto)
        self.assertIn('cierra 10/10 (3 días)', texto)
        self.assertIn('Quechua &lt;b&gt;Central&lt;/b&gt;', texto)  # el HTML del título no se cuela

    def test_html_del_informe(self):
        h = informe.construir_html(HOY, self.datos(), [{'nombre': 'OEA · becas', 'url': 'https://x.org/a?b=1&c=2', 'lineas': ['Abierta la convocatoria 2027']}], ['PRONABEC: tiempo agotado'], CFG)
        self.assertIn('Informe del miércoles 7 de octubre de 2026', h)
        self.assertIn('Becas · 1', h)
        self.assertIn('Cursos y capacitaciones · 1', h)
        self.assertIn('Quechua &lt;b&gt;Central&lt;/b&gt;', h)
        self.assertIn('Por confirmar', h)
        self.assertIn('class="pronto"', h)  # le quedan 3 días
        self.assertIn('href="https://x.org/a?b=1&amp;c=2"', h)
        self.assertIn('PRONABEC: tiempo agotado', h)
        self.assertIn('2 oportunidades nuevas', h)
        self.assertIn('1 gratuita', h)

    def test_crea_un_pdf_de_verdad(self):
        try:
            informe.buscar_navegador()
        except informe.ErrorInforme:
            self.skipTest('no hay Edge ni Chrome en esta PC')
        ruta = os.path.join(tempfile.mkdtemp(), 'prueba.pdf')
        informe.html_a_pdf(informe.construir_html(HOY, self.datos(), [], [], CFG), ruta)
        with open(ruta, 'rb') as f:
            datos = f.read()
        self.assertTrue(datos.startswith(b'%PDF'))
        self.assertGreater(len(datos), 5000)

    def test_telegram_parte_mensajes_largos(self):
        ms = telegram.partir([f'bloque {i} ' + 'x' * 900 for i in range(10)], 3800)
        self.assertTrue(all(len(m) <= 3800 for m in ms))


class TestRuidoDeNoticias(unittest.TestCase):
    """20/10/2026: de 50 candidatas en 8 días, ~40 eran notas de prensa o cosas solo para el personal de una entidad."""
    HOY_R = date(2026, 10, 20)

    def test_las_noticias_de_algo_que_ya_paso_o_que_solo_informa_no_pasan(self):
        for titulo in [
            'Hospital María Auxiliadora inició su II Curso Taller Semipresencial de Lactancia Materna 2026',
            'Más de 100 voluntarios participaron en jornada de limpieza del río Locumba en Tacna',
            'Sunedu fortalece orientación técnica a la Ensap para agilizar el registro de programas, grados y títulos de posgrado',
            'Minsa: SIS obtiene certificación de tres buenas prácticas en calidad de servicios públicos',
            'Caral Raymi 2026: culminó con éxito el primer taller de octubre y quedan dos más',
            'Rumbo al Día Mundial del ACV realizamos capacitación para fortalecer la atención oportuna del accidente cerebrovascular',
            'DF de la Selva Central realizó taller de prevención sobre la violencia en la familia en una comunidad nativa de Satipo',
            'Pensionistas ONP aprenden IA y envían mensajes de aliento al Papa León',
            'Abancay aprende a cuidar el agua potable desde el mercado, la universidad y las aulas',
            'Huánuco: Productores del Alto Huallaga aprenderán nuevas técnicas para el cultivo de cacao',
            'Coneau reunirá a especialistas para analizar el futuro de las microcredenciales y la certificación de competencias profesionales',
            'Pronabec y la Embajada de Australia abordan oportunidades educativas de posgrado para peruanos',
            'Más de 700 estudiantes de hogares usuarios del programa Juntos accedieron a Beca 18',
            'Justicia Juvenil Restaurativa de Chorrillos brinda capacitación a comunidad educativa de la I.E.P. José Olaya Balandra',
            'Coordina capacitaciones para fortalecer la lactancia materna',
            'Una ruta común permite articular mejor la formación y el empleo',
            'MTPE y UNICEF lanzan convocatoria para el desarrollo de cursos virtuales dirigidos a beneficiarios del programa Jóvenes Productivos',
            'SENCICO acerca oportunidades de capacitación técnica a trabajadores de la construcción en Feria del PRO de Promart Homecenter',
            'Ministerio de Salud lanza primer premio nacional para impulsar la investigación en envejecimiento y demencias',
            'Libro “Reconocimiento constitucional del derecho al olvido” será presentado este jueves 15 de octubre en conversatorio organizado por el CEC',
        ]:
            self.assertFalse(clasificar.es_oportunidad(titulo, self.HOY_R), titulo)

    def test_las_oportunidades_reales_siguen_pasando(self):
        for titulo in [
            'Curso sobre “Protección de datos personales: autodeterminación informativa, derecho al olvido y mecanismos de tutela” desde el 21 de octubre',
            'OFIS lanza Aprende OFIS, su nueva plataforma virtual de capacitación en focalización e información social',
            'UNATECH convoca a foro sobre gestión del riesgo de desastres y cambio climático',
            'Charla virtual gratuita: Control metrológico de balanzas en mercados',
            'Pronabec ofrece 6000 nuevas vacantes de Beca 18 para estudiar carreras acordes con las necesidades del país',
            'MINJUSDH: Gobierno otorgará becas Repared para estudiar en universidades e institutos',
            'Premio Nacional de Tesis para estudiantes universitarios 2026',
        ]:
            self.assertTrue(clasificar.es_oportunidad(titulo, self.HOY_R), titulo)

    def test_los_hospitales_nacionales_cuentan_como_locales(self):
        for slug in ['hnch', 'hnseb', 'hma', 'hlev']:
            self.assertTrue(clasificar.es_local(slug), slug)
        self.assertFalse(clasificar.es_local('pronabec'))

    def test_la_pagina_que_es_solo_para_personal_se_descarta(self):
        sbn = '<p>Dirigido a: funcionarios, servidores civiles, practicantes y locadores de servicios que gestionan predios estatales. Se debe adjuntar un oficio de la entidad que le acredite para participar.</p>'
        ins = '<p>La convocatoria está dirigida al personal de salud que mantenga vínculo laboral bajo nombramiento o CAS.</p>'
        ofis = '<p>Cursos dirigidos a servidores públicos, la comunidad académica y la ciudadanía.</p>'
        self.assertTrue(clasificar.analizar_pagina(sbn, self.HOY_R).get('soloPersonal'))
        self.assertTrue(clasificar.analizar_pagina(ins, self.HOY_R).get('soloPersonal'))
        self.assertFalse(clasificar.analizar_pagina(ofis, self.HOY_R).get('soloPersonal'))
        with mock.patch.object(clasificar, 'leer_pagina', return_value={'soloPersonal': True}):
            self.assertIsNone(seleccion.candidato_desde(item('Curso Virtual de Regímenes Especiales de la Propiedad Estatal', 'sbn'), self.HOY_R))


if __name__ == '__main__':
    unittest.main()
