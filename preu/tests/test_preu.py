"""Pruebas del «Bot Preu» sin red: páginas guardadas del PRONABEC (21/10/2026) y un Telegram falso.
Correr: python -m unittest discover -s tests   (desde la carpeta preu)"""
import json
import os
import sys
import tempfile
import types
import unittest
from unittest import mock

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import bot  # noqa: E402
import enlaces  # noqa: E402
import pronabec  # noqa: E402


def leer(nombre):
    with open(os.path.join(AQUI, 'fixtures', nombre), encoding='utf-8') as fh:
        return fh.read()


class TelegramFalso:
    chat_id = '111'

    def __init__(self, toques=()):
        self.enviados, self.editados, self.respuestas, self._toques = [], [], [], list(toques)

    def enviar(self, texto):
        self.enviados.append(texto)

    def enviar_con_botones(self, texto, botones):
        self.enviados.append((texto, botones))
        return 42

    def editar(self, mid, texto):
        self.editados.append((mid, texto))

    def actualizaciones(self, offset):
        return [t for t in self._toques if t['update_id'] >= offset]

    def responder_toque(self, id_toque, texto):
        self.respuestas.append(texto)


def toque(uid, data, de='111'):
    return {'update_id': uid, 'callback_query': {'id': f'q{uid}', 'data': data, 'from': {'id': de}, 'message': {'chat': {'id': de}}}}


class Pronabec(unittest.TestCase):
    def test_lee_el_cronograma_de_beca18(self):
        c = pronabec.leer_cronograma(leer('beca-18.html'))
        self.assertEqual(c['convocatoria'], 'Convocatoria 2027')
        self.assertEqual(c['cronograma'][0], {'que': 'Inscripción al ENP', 'desde': '2026-10-09', 'hasta': '2026-10-18'})
        self.assertEqual(c['cronograma'][3], {'que': 'Aplicación del ENP', 'desde': '2026-11-22', 'hasta': '2026-11-22'})
        self.assertEqual(len(c['cronograma']), 5)
        self.assertTrue(pronabec.es_publicable(c))

    def test_si_cambia_el_diseno_no_inventa(self):
        self.assertIsNone(pronabec.leer_cronograma('<html><body>Página nueva sin cronograma</body></html>'))
        c = pronabec.leer_cronograma('<p>CRONOGRAMA</p><p>Pronto anunciaremos las fechas</p><p>REQUISITOS</p>')
        self.assertEqual(c['cronograma'], [])
        self.assertFalse(pronabec.es_publicable(c))

    def test_la_firma_cambia_si_cambian_las_fechas(self):
        c = pronabec.leer_cronograma(leer('beca-18.html'))
        otra = json.loads(json.dumps(c))
        otra['cronograma'][3]['desde'] = otra['cronograma'][3]['hasta'] = '2026-11-29'
        self.assertNotEqual(pronabec.firma(c), pronabec.firma(otra))
        self.assertEqual(pronabec.firma(c), pronabec.firma(json.loads(json.dumps(c))))

    def test_concursos_en_proceso_solo_esa_seccion(self):
        urls = [c['url'] for c in pronabec.concursos_en_proceso(leer('concursos.html'))]
        self.assertEqual(urls, ['https://www.pronabec.gob.pe/beca-18/', 'https://www.pronabec.gob.pe/beca-generacion-bicentenario/'])
        self.assertEqual(pronabec.concursos_en_proceso('<html>sin sección</html>'), [])
        self.assertEqual(pronabec.titulo_de(leer('beca-18.html')), 'Beca 18')


class Enlaces(unittest.TestCase):
    def test_avisa_solo_tras_dos_semanas_y_cuando_vuelve(self):
        lista = [{'url': 'https://a.pe/', 'nombre': 'A'}, {'url': 'https://b.pe/', 'nombre': 'B'}]
        mem = {}
        caido = lambda url: (url != 'https://b.pe/', '503')  # noqa: E731
        self.assertEqual(enlaces.revisar(lista, mem, caido)[0], [])  # 1.ª semana: todavía no
        caidos, _, ok = enlaces.revisar(lista, mem, caido)
        self.assertEqual([c[0] for c in caidos], ['B'])
        self.assertEqual(ok, 1)
        self.assertEqual(enlaces.revisar(lista, mem, caido)[0], [])  # no se repite el aviso
        _, recuperados, _ = enlaces.revisar(lista, mem, lambda url: (True, '200'))
        self.assertEqual([r[0] for r in recuperados], ['B'])

    def test_olvida_enlaces_que_ya_no_estan(self):
        mem = {'https://viejo.pe/': {'fallos': 3, 'avisado': True}}
        enlaces.revisar([{'url': 'https://a.pe/'}], mem, lambda url: (True, '200'))
        self.assertNotIn('https://viejo.pe/', mem)


class Flujo(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.parche = mock.patch.object(bot, 'ESTADO', os.path.join(self.dir, 'estado.json'))
        self.parche.start()

    def tearDown(self):
        self.parche.stop()

    def test_primera_vez_aprende_y_luego_pide_aprobacion_si_cambia(self):
        estado, tg = bot.estado_inicial(), TelegramFalso()
        html = leer('beca-18.html')
        with mock.patch.object(bot, 'descargar', return_value=html):
            bot.vigilar_beca18(tg, estado, [])
            self.assertEqual(tg.enviados, [])  # punto de partida: no avisa
            bot.vigilar_beca18(tg, estado, [])
            self.assertEqual(tg.enviados, [])  # sin cambios
        with mock.patch.object(bot, 'descargar', return_value=html.replace('22/11/2026', '29/11/2026')):
            bot.vigilar_beca18(tg, estado, [])
        texto, botones = tg.enviados[0]
        self.assertIn('29/11/2026', texto)
        self.assertTrue(botones[0][0][1].startswith('b18pub:'))
        self.assertEqual(estado['beca18']['pendiente']['estado'], 'pendiente')

    def _con_pendiente(self):
        estado = bot.estado_inicial()
        datos = {'convocatoria': 'Convocatoria 2028', 'cronograma': [{'que': 'Examen', 'desde': '2027-11-22', 'hasta': '2027-11-22'}], 'revisado': '2027-10-05'}
        estado['beca18']['pendiente'] = {'clave': 'abc', 'datos': datos, 'estado': 'pendiente', 'mensaje': 42, 'enviado': bot.hoy_peru().isoformat()}
        return estado

    def test_solo_el_admin_aprueba_y_se_publica_con_el_publicador(self):
        estado = self._con_pendiente()
        tg = TelegramFalso([toque(1, 'b18pub:abc', de='999'), toque(2, 'b18pub:abc')])
        llamadas = []

        def ejecutar(cmd, **kw):
            with open(cmd[-1], encoding='utf-8') as fh:
                llamadas.append(json.load(fh))
            return types.SimpleNamespace(stdout='RESUMEN {"estado": "publicada"}', stderr='')
        with mock.patch.object(bot.telegram, 'cargar_env', return_value={'UNINEXO_BOT_PASSWORD': 'x'}), \
                mock.patch.object(bot, 'comando_publicador', side_effect=lambda cfg, ruta: (['node', 'p.mjs', ruta], self.dir)):
            r = bot.aprobaciones(tg, estado, {}, ejecutar)
        self.assertIn('Solo el administrador', tg.respuestas[0])
        self.assertEqual(llamadas[0]['convocatoria'], 'Convocatoria 2028')
        self.assertEqual(estado['beca18']['pendiente']['estado'], 'publicada')
        self.assertIn('publicada', r)
        self.assertEqual(estado['offset'], 3)

    def test_si_falla_queda_aprobada_para_reintentar(self):
        estado = self._con_pendiente()
        tg = TelegramFalso([toque(5, 'b18pub:abc')])
        falla = lambda cmd, **kw: types.SimpleNamespace(stdout='RESUMEN {"estado": "fallida", "motivo": "sin red"}', stderr='')  # noqa: E731
        with mock.patch.object(bot.telegram, 'cargar_env', return_value={'UNINEXO_BOT_PASSWORD': 'x'}), \
                mock.patch.object(bot, 'comando_publicador', side_effect=lambda cfg, ruta: (['node', 'p.mjs', ruta], self.dir)):
            bot.aprobaciones(tg, estado, {}, falla)
        self.assertEqual(estado['beca18']['pendiente']['estado'], 'aprobada')
        self.assertTrue(any('No pude publicar' in t for t in tg.enviados))

    def test_descartar_no_publica(self):
        estado = self._con_pendiente()
        tg = TelegramFalso([toque(1, 'b18des:abc')])
        bot.aprobaciones(tg, estado, {}, lambda *a, **k: self.fail('no debía publicar'))
        self.assertEqual(estado['beca18']['pendiente']['estado'], 'descartada')


if __name__ == '__main__':
    unittest.main()
