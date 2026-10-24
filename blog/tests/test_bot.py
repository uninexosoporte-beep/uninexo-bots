import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import bot  # noqa: E402

CHAT = '111'


class TgFalso:
    def __init__(self):
        self.chat_id, self.toques, self.enviados, self.editados, self.respuestas = CHAT, [], [], [], []

    def actualizaciones(self, offset):
        return [u for u in self.toques if u['update_id'] >= offset]

    def enviar_con_botones(self, texto, botones):
        self.enviados.append((texto, botones))
        return 500 + len(self.enviados)

    def enviar(self, texto):
        self.enviados.append((texto, None))

    def editar(self, mensaje, texto):
        self.editados.append((mensaje, texto))

    def responder_toque(self, id_toque, texto):
        self.respuestas.append(texto)

    def tocar(self, data, de=CHAT, uid=1):
        self.toques.append({'update_id': uid, 'callback_query': {'id': f'q{uid}', 'data': data, 'from': {'id': de}, 'message': {'chat': {'id': de}}}})


class BloggerFalso:
    def __init__(self, falla=False):
        self.llamadas, self.falla = [], falla

    def publicar(self, e, post_id=None):
        if self.falla:
            raise RuntimeError('Blogger respondió 500')
        self.llamadas.append((e['uniId'], post_id))
        return post_id or f'p-{e["uniId"]}', f'https://blog.uninexo.link/{e["uniId"]}.html'


def entrada(uni, huella='h1'):
    return {'uniId': uni, 'titulo': f'Grupos de la {uni}', 'descripcion': 'd', 'etiquetas': [uni], 'html': '<p>x</p>', 'huella': huella}


class PruebasBot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        bot.ESTADO = os.path.join(self.tmp.name, 'estado.json')
        self.estado = bot.estado_inicial()
        self.tg, self.bl = TgFalso(), BloggerFalso()
        self.entradas = {'unmsm': entrada('unmsm'), 'uni': entrada('uni')}

    def tearDown(self):
        self.tmp.cleanup()

    def vuelta(self):
        return bot.vuelta(self.tg, self.bl, self.estado, entradas_fn=lambda: self.entradas, hora_minima=0)

    def test_propone_una_por_dia(self):
        self.vuelta()
        self.assertEqual(self.estado['pendiente']['uni'], 'unmsm')
        self.vuelta()
        self.assertEqual(len(self.tg.enviados), 1)

    def test_aprobar_publica_y_no_duplica(self):
        self.vuelta()
        self.tg.tocar('blgpub:unmsm')
        self.vuelta()
        self.assertEqual(self.bl.llamadas, [('unmsm', None)])
        self.assertEqual(self.estado['publicadas']['unmsm']['post_id'], 'p-unmsm')
        # Cambian los datos: al otro día propone ACTUALIZAR (PATCH con el mismo id), después de las nuevas
        self.estado['ultima_propuesta'] = ''
        self.vuelta()
        self.assertEqual(self.estado['pendiente']['uni'], 'uni')
        self.estado['publicadas']['uni'] = {'post_id': 'p-uni', 'url': 'u', 'huella': 'h1'}
        self.estado['pendiente']['estado'] = 'publicada'
        self.entradas['unmsm'] = entrada('unmsm', 'h2')
        self.estado['ultima_propuesta'] = ''
        self.vuelta()
        self.assertIn('Actualizar', self.tg.enviados[-1][0])
        self.tg.tocar('blgpub:unmsm', uid=2)
        self.vuelta()
        self.assertEqual(self.bl.llamadas[-1], ('unmsm', 'p-unmsm'))

    def test_saltar_no_vuelve_hasta_que_cambie(self):
        self.vuelta()
        self.tg.tocar('blgdes:unmsm')
        self.estado['ultima_propuesta'] = ''
        self.vuelta()
        self.assertEqual(self.estado['pendiente']['uni'], 'uni')
        self.assertEqual(self.bl.llamadas, [])

    def test_toque_ajeno_no_vale(self):
        self.vuelta()
        self.tg.tocar('blgpub:unmsm', de='999')
        self.vuelta()
        self.assertEqual(self.bl.llamadas, [])
        self.assertEqual(self.estado['pendiente']['estado'], 'pendiente')

    def test_falla_de_blogger_se_reintenta(self):
        self.vuelta()
        self.tg.tocar('blgpub:unmsm')
        self.bl.falla = True
        self.vuelta()
        self.assertEqual(self.estado['pendiente']['estado'], 'aprobada')
        self.bl.falla = False
        self.vuelta()
        self.assertEqual(self.estado['pendiente']['estado'], 'publicada')


if __name__ == '__main__':
    unittest.main()
