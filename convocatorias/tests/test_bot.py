"""Pruebas del bot de Convocatorias (sin internet). Correr con:  python -m unittest discover -s tests -v   (desde D:\\uninexo-bot-convocatorias)"""
import json
import os
import sys
import unittest
from datetime import date
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bot  # noqa: E402
import clasificar  # noqa: E402
import gobpe  # noqa: E402
import informe  # noqa: E402
import mensajes  # noqa: E402
import publicado  # noqa: E402
import reglas  # noqa: E402
import seleccion  # noqa: E402

HOY = date(2026, 10, 8)
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json'), encoding='utf-8') as _f:
    CFG = json.load(_f)

# Los campos que acepta la regla `isValidConvocatoriaData` de la app (lo que importa el botón «Importar del bot»)
CAMPOS_PERMITIDOS = {'title', 'organization', 'category', 'sector', 'location', 'description', 'officialUrl', 'deadline', 'modalidad'}


def cfg_con(**reglas_):
    c = json.loads(json.dumps(CFG))
    c['reglas'] = {'tipos': {}, 'instituciones': {}}
    c['reglas'].update(reglas_)
    return c


def item(titulo='Programa de voluntariado juvenil 2026', slug='reniec', fecha='2026-10-07', fuente='gobpe-campañas'):
    return {'titulo': titulo, 'url': f'https://www.gob.pe/institucion/{slug}/campa%C3%B1as/123-x', 'fecha': fecha, 'slug': slug, 'fuente': fuente}


def cand(titulo='Programa de voluntariado juvenil 2026', slug='reniec', **extra):
    c = seleccion.candidato_desde(item(titulo, slug), HOY, leer_pagina=False)
    c.update(extra)
    return c


class TestClasificar(unittest.TestCase):
    def test_tipo_por_el_titulo(self):
        casos = {
            'Ciberseminarios en Voluntariado 2026': 'voluntariado',
            'Programa Nacional de Voluntariado Universitario': 'voluntariado',
            'Convocatoria Practicas N° 064-2026 PRACTICANTE PROFESIONAL - OEE': 'practicas',
            'Concurso Público de Prácticas N° 012-2026': 'practicas',
            'Prácticas preprofesionales Nº 018-2026': 'practicas',
            'Pasantías SERVIR': 'practicas',
            'Empleo part time para universitarios': 'part_time',
            'Feria laboral para jóvenes de Lima': 'full_time',
            'Jóvenes Productivos': 'full_time',
            'Convocatoria de personal CAS N° 012-2026': 'cas',
        }
        for titulo, tipo in casos.items():
            self.assertEqual(clasificar.tipo_de(titulo), tipo, titulo)

    def test_no_es_convocatoria_lo_que_es_resultado_ruido_o_buenas_practicas(self):
        for titulo in ['Resultados del concurso de prácticas N° 012-2026', 'Prácticas profesionales Nº 002-2026 (CONCLUIDO)', 'Lista de admitidos al voluntariado',
                       'Buenas prácticas agrícolas en cacao', 'Concurso Nacional de Buenas Prácticas Docente 2026', 'Prácticas ambientales en la escuela',
                       'Ceremonia de clausura del voluntariado', 'Comunicado: reprogramación de prácticas', 'Servicio militar voluntario', 'Cuadro multianual de necesidades']:
            self.assertFalse(clasificar.es_oportunidad(titulo, HOY), titulo)
        self.assertTrue(clasificar.es_oportunidad('Voluntariado Individual de la Identificación', HOY))
        self.assertTrue(clasificar.es_oportunidad('Convocatoria Practicas N° 064-2026 PRACTICANTE PROFESIONAL - OEE', HOY))

    def test_una_noticia_solo_cuenta_si_su_titulo_invita_a_hacer_algo(self):
        # pasó en la simulación del 08/10/2026: una noticia de una universidad sobre una pasantía ya hecha salía como convocatoria
        hecha = 'Estudiantes de la UNAH participan en pasantía académica inclusiva'
        self.assertFalse(clasificar.es_oportunidad(hecha, HOY, 'gobpe-noticias'))
        self.assertTrue(clasificar.es_oportunidad(hecha, HOY, 'gobpe-campañas'))  # una campaña es un programa, no un hecho
        self.assertTrue(clasificar.es_oportunidad('Senaju convoca a postular al voluntariado juvenil 2027', HOY, 'gobpe-noticias'))
        self.assertTrue(clasificar.es_oportunidad('Abren inscripciones para el programa de voluntariado de RENIEC', HOY, 'gobpe-noticias'))
        self.assertFalse(clasificar.es_oportunidad('RENIEC realizó jornada de voluntariado en Cusco', HOY, 'gobpe-noticias'))
        self.assertIsNone(seleccion.candidato_desde(item(hecha, 'unah', fuente='gobpe-noticias'), HOY, leer_pagina=False))

    def test_una_fecha_vencida_en_el_titulo_es_un_evento_que_ya_paso(self):
        self.assertFalse(clasificar.es_oportunidad('Jornada de voluntariado 28/08/2026', HOY))
        self.assertTrue(clasificar.es_oportunidad('Jornada de voluntariado 28/10/2026', HOY))

    def test_region_del_titulo_o_todo_el_peru(self):
        self.assertEqual(clasificar.region_de('Voluntariado en Madre de Dios 2026'), 'Madre de Dios')
        self.assertEqual(clasificar.region_de('Feria laboral Arequipa'), 'Arequipa')
        self.assertEqual(clasificar.region_de('Programa de voluntariado juvenil'), 'Todo el Perú')

    def test_fecha_limite_y_modalidad_de_la_pagina(self):
        html = ('<meta name="description" content="Postula al programa de voluntariado y gana experiencia con certificado de horas.">'
                '<p>Las inscripciones son hasta el 25 de octubre de 2026. Actividades presenciales y virtuales.</p>')
        datos = clasificar.analizar_pagina(html, HOY)
        self.assertEqual(datos['fechaLimite'], '2026-10-25')
        self.assertEqual(datos['modalidad'], 'hibrido')
        self.assertIn('programa de voluntariado', datos['descripcion'])
        self.assertNotIn('fechaLimite', clasificar.analizar_pagina('<p>Programa permanente sin fecha.</p>', HOY))
        self.assertNotIn('fechaLimite', clasificar.analizar_pagina('<p>Inscripciones hasta el 3 de setiembre de 2026.</p>', HOY))  # ya pasó


class TestReglas(unittest.TestCase):
    def test_por_defecto_ignora_los_cas_y_acepta_lo_demas(self):
        self.assertIsNone(reglas.evaluar(cand(), CFG, HOY))
        cas = cand('Convocatoria CAS N° 012-2026 Asistente', 'servir')
        self.assertEqual(cas['tipo'], 'cas')
        self.assertIsNotNone(reglas.evaluar(cas, CFG, HOY))

    def test_solo_ciertos_tipos(self):
        cfg = cfg_con(tipos={'solo': ['voluntariado']})
        self.assertIsNone(reglas.evaluar(cand(), cfg, HOY))
        self.assertIsNotNone(reglas.evaluar(cand('Prácticas pre profesionales 2026', 'mimp'), cfg, HOY))

    def test_instituciones_locales_se_ignoran_salvo_que_las_incluyas(self):
        self.assertFalse(reglas.institucion_permitida('munilima', CFG))
        self.assertFalse(reglas.institucion_permitida('ugel07', CFG))
        self.assertTrue(reglas.institucion_permitida('unamad', CFG))
        self.assertTrue(reglas.institucion_permitida('reniec', CFG))
        self.assertTrue(reglas.institucion_permitida('munilima', cfg_con(incluir_locales=True)))

    def test_si_cierra_muy_pronto_o_ya_cerro_no_se_avisa(self):
        self.assertIsNotNone(reglas.evaluar(cand(fechaLimite='2026-10-08'), CFG, HOY))
        self.assertIsNotNone(reglas.evaluar(cand(fechaLimite='2026-10-09'), CFG, HOY))
        self.assertIsNone(reglas.evaluar(cand(fechaLimite='2026-10-20'), CFG, HOY))


class TestSeleccionYDocumento(unittest.TestCase):
    def test_documento_solo_trae_campos_de_la_regla_de_la_app(self):
        for c in [cand(fechaLimite='2026-10-25', modalidad='hibrido'), cand('Feria laboral Arequipa', 'mtpe'), seleccion.a_entidad(cand('Convocatoria Practicas N° 064-2026', 'indecopi'))]:
            d = seleccion.documento(c, HOY)
            self.assertTrue(set(d) <= CAMPOS_PERMITIDOS, set(d) - CAMPOS_PERMITIDOS)
            self.assertTrue(d['officialUrl'].startswith('https://'))
            self.assertIn(d['category'], clasificar.TIPOS)
            self.assertEqual(d['sector'], 'Sector Público')
            self.assertTrue(3 <= len(d['title']) <= 200 and 2 <= len(d['organization']) <= 120 and len(d['description']) <= 3000 and len(d['location']) <= 100)
            self.assertNotIn('groupUrl', d)  # no se inventan grupos
            self.assertIn('Revisa las bases', d['description'])
        d = seleccion.documento(cand(fechaLimite='2026-10-25', modalidad='hibrido'), HOY)
        self.assertEqual((d['deadline'], d['modalidad']), ('2026-10-25', 'Híbrido'))
        self.assertNotIn('deadline', seleccion.documento(cand(), HOY))

    def test_el_nombre_del_autor_del_bot_no_es_un_nombre_reservado(self):
        for palabra in ['admin', 'oficial', 'uninexo', 'moderador', 'soporte']:
            self.assertNotIn(palabra, seleccion.AUTOR_BOT.lower())

    def test_una_convocatoria_de_practicas_se_vuelve_ficha_de_la_entidad(self):
        c = seleccion.a_entidad(cand('Convocatoria Practicas N° 064-2026 PRACTICANTE PROFESIONAL - OEE', 'indecopi'))
        self.assertEqual(c['name'], 'Prácticas pre y profesionales en INDECOPI')
        self.assertTrue(c['entidad'])
        self.assertIsNone(c['fechaLimite'])
        self.assertIn('N° 064-2026', c['descripcion'])
        self.assertEqual(seleccion.clave_entidad(c), 'e:indecopi')

    def test_orden_voluntariados_primero_y_luego_lo_que_cierra_antes(self):
        a, b, c = cand('Prácticas pre profesionales 2026', 'mimp'), cand('Voluntariado juvenil', 'reniec'), cand('Voluntariado en el Perú', 'minam', fechaLimite='2026-10-20')
        self.assertEqual([x['institucion'] for x in sorted([a, b, c], key=seleccion.prioridad)], ['Ministerio del Ambiente', 'RENIEC', 'MIMP'])

    def test_url_canonica_ignora_www_barra_final_y_mayusculas(self):
        self.assertEqual(seleccion.url_canonica('https://www.GOB.pe/institucion/mimp/campañas/12-x/'), seleccion.url_canonica('http://gob.pe/institucion/mimp/campañas/12-x'))

    def test_lectura_de_la_lista_de_campanas(self):
        t = ('<ul><li><a href="/institucion/reniec/campa%C3%B1as/145-voluntariado-individual">Voluntariado Individual de la Identificación</a><time datetime="2026-09-03 08:00:00.000"> 3 de setiembre de 2026</time></li>'
             '<li><a href="/institucion/reniec/informes-publicaciones/9-otro">Otro</a></li></ul>')
        r = gobpe.leer_tarjetas_campanas(t, 'reniec')
        self.assertEqual(len(r), 1)
        self.assertEqual((r[0]['titulo'], r[0]['fecha'], r[0]['slug']), ('Voluntariado Individual de la Identificación', '2026-09-03', 'reniec'))

    def test_la_busqueda_ignora_un_resultado_null_de_gobpe(self):
        # pasó el 08/10/2026 con «especialización» (bot de Cursos): gob.pe mandó null en medio de la lista y la búsqueda entera fallaba
        bueno = {'url': '<a href="/institucion/reniec/campa%C3%B1as/145-voluntariado">Voluntariado</a>', 'publication': 'Publicado el 1 de julio de 2026'}
        cuerpo = json.dumps({'data': {'attributes': {'results': [None, bueno, None]}}})
        with mock.patch.object(gobpe, 'descargar', return_value=cuerpo):
            r = gobpe.buscar('voluntariado', 'campañas', pausa=0)
        self.assertEqual([x['fecha'] for x in r], ['2026-07-01'])


class TestPublicado(unittest.TestCase):
    PUB = {'urls': {'gob.pe/institucion/indecopi/colecciones/40050-convocatorias-de-modalidades-formativas-practicas'},
           'convocatorias': [('Prácticas pre y profesionales en INDECOPI', 'INDECOPI'), ('Voluntariado en la Cruz Roja Peruana', 'Cruz Roja Peruana'),
                             ('Prácticas pre y profesionales en SERVIR', 'SERVIR · Talento Perú')],
           'slugs': {'indecopi', 'servir'}}

    def test_reconoce_lo_ya_publicado_por_enlace(self):
        c = cand('Programa de voluntariado juvenil', 'reniec')
        c['enlaceOficial'] = 'https://www.gob.pe/institucion/indecopi/colecciones/40050-convocatorias-de-modalidades-formativas-practicas/'
        self.assertTrue(publicado.ya_publicada(c, self.PUB))
        self.assertFalse(publicado.ya_publicada(cand(), self.PUB))

    def test_una_entidad_que_ya_esta_no_se_vuelve_a_proponer_pero_una_nueva_si(self):
        indecopi = seleccion.a_entidad(cand('Convocatoria Practicas N° 065-2026', 'indecopi'))
        servir = seleccion.a_entidad(cand('Convocatoria de Prácticas N° 025-2026', 'servir'))
        mimp = seleccion.a_entidad(cand('Prácticas preprofesionales Nº 094-2026', 'mimp'))
        self.assertTrue(publicado.ya_publicada(indecopi, self.PUB))  # por el slug del enlace
        self.assertTrue(publicado.ya_publicada(servir, self.PUB))
        self.assertFalse(publicado.ya_publicada(mimp, self.PUB))
        sin_nada = {'urls': set(), 'convocatorias': [('Voluntariado', 'Cruz Roja Peruana')], 'slugs': set()}
        self.assertTrue(publicado.entidad_conocida(seleccion.a_entidad(cand('Prácticas pre profesionales', 'servir')), {'urls': set(), 'convocatorias': [('x', 'SERVIR · Talento Perú')], 'slugs': set()}))  # por el nombre
        self.assertFalse(publicado.entidad_conocida(mimp, sin_nada))

    def test_una_convocatoria_casi_igual_de_la_misma_entidad_cuenta_como_repetida(self):
        pub = {'urls': set(), 'convocatorias': [('Programa Nacional de Voluntariado Universitario del Ministerio Público', 'Ministerio Público')], 'slugs': {'mpfn'}}
        c = cand('Programa Nacional de Voluntariado Universitario del Ministerio Público 2026', 'mpfn')
        self.assertTrue(publicado.ya_publicada(c, pub))


class TestBot(unittest.TestCase):
    def test_las_practicas_por_documento_van_por_entidad_y_el_resto_una_por_una(self):
        self.assertTrue(bot.es_practica_de_entidad(item('Convocatoria Practicas N° 064-2026', 'indecopi', fuente='gobpe-publicaciones')))
        self.assertFalse(bot.es_practica_de_entidad(item('Pasantías SERVIR', 'servir', fuente='gobpe-campañas')))
        self.assertFalse(bot.es_practica_de_entidad(item('Programa de voluntariado juvenil', 'reniec', fuente='gobpe-publicaciones')))


class TestMensajesEInforme(unittest.TestCase):
    def datos(self):
        return [cand('Voluntariado Individual de la Identificación <b>2026</b>', 'reniec', fechaLimite='2026-10-12', modalidad='presencial'),
                seleccion.a_entidad(cand('Convocatoria Practicas N° 064-2026', 'indecopi'))]

    def test_mensajes_con_el_distintivo_de_convocatorias(self):
        t = mensajes.mensaje_resumen(HOY, 2, 1, 0, [], 20, con_pdf=True)
        self.assertTrue(t.startswith('💼'))
        self.assertIn('detalle va en el PDF', t)
        self.assertTrue(mensajes.mensaje_resumen(HOY, 0, 0, 0, [], 20).startswith('💼'))
        self.assertTrue(mensajes.mensaje_inicial(100, 4).startswith('💼'))
        texto = '\n'.join(mensajes.bloques_candidatos(self.datos(), HOY))
        self.assertIn('cierra 12/10 (4 días)', texto)
        self.assertIn('entidad nueva en UniNexo', texto)
        self.assertIn('2026&lt;/b&gt;', texto)  # el HTML del título no se cuela

    def test_html_del_informe(self):
        h = informe.construir_html(HOY, self.datos(), [{'nombre': 'SENAJU · voluntariado', 'url': 'https://x.org/a?b=1&c=2', 'lineas': ['Abierta la convocatoria 2027']}], ['SENAJU: tiempo agotado'], CFG)
        self.assertIn('Informe del jueves 8 de octubre de 2026', h)
        self.assertIn('Voluntariados · 1', h)
        self.assertIn('Prácticas pre y profesionales · 1', h)
        self.assertIn('Entidad nueva en UniNexo', h)
        self.assertIn('class="pronto"', h)  # le quedan 4 días
        self.assertIn('href="https://x.org/a?b=1&amp;c=2"', h)
        self.assertIn('SENAJU: tiempo agotado', h)
        self.assertNotIn('Costo', h)


if __name__ == '__main__':
    unittest.main()
