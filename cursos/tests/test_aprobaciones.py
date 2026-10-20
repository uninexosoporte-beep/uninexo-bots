"""Pruebas de la aprobación de cursos por Telegram (sin internet: Telegram y el publicador se simulan)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aprobaciones  # noqa: E402

HOY = date(2026, 10, 20)
DUENO = '555'


class TelegramFalso:
    def __init__(self):
        self.chat_id = DUENO
        self.enviados, self.editados, self.respuestas, self.toques = [], {}, [], []
        self.siguiente = 100

    def enviar_con_botones(self, texto, botones):
        self.siguiente += 1
        self.enviados.append((self.siguiente, texto, botones))
        return self.siguiente

    def enviar(self, texto):
        self.enviados.append((None, texto, None))

    def actualizaciones(self, offset):
        return [u for u in self.toques if u['update_id'] >= offset]

    def responder_toque(self, id_toque, texto):
        self.respuestas.append(texto)

    def editar(self, id_mensaje, texto):
        self.editados[id_mensaje] = texto

    def tocar(self, data, de=DUENO, chat=DUENO):
        n = len(self.toques) + 1
        self.toques.append({'update_id': n, 'callback_query': {'id': f'q{n}', 'data': data, 'from': {'id': int(de)}, 'message': {'chat': {'id': int(chat)}}}})


def doc(n, **extra):
    d = {'name': f'Curso virtual gratuito número {n}', 'career': 'Derecho y Ciencias Políticas', 'region': 'Todo el país', 'tipo': 'curso',
         'enlaceOficial': f'https://www.gob.pe/institucion/tc/noticias/{n}-curso', 'institucion': 'TC', 'gratuito': True, 'description': 'Curso gratis.'}
    d.update(extra)
    return d


class TestAprobaciones(unittest.TestCase):
    def setUp(self):
        self.aqui = tempfile.mkdtemp()
        self.tg = TelegramFalso()
        cred = os.path.join(self.aqui, 'cred.env')
        open(cred, 'w').write('UNINEXO_BOT_PASSWORD=secreta\nUNINEXO_BOT_APPCHECK_DEBUG=t\n')
        self.proyecto = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.proyecto, 'scripts'))
        open(os.path.join(self.proyecto, 'scripts', 'publicar-cursos-bot.ts'), 'w').write('')
        self.cfg = {'aprobacion_telegram': {'activa': True, 'proyecto': self.proyecto, 'credenciales': cred, 'dias_vigencia': 14}}
        self.llamadas = []

    def publicador(self, estado='publicada'):
        def falso(cmd, **kw):
            enviados = json.load(open(cmd[-1], encoding='utf-8'))
            self.llamadas.append((enviados, kw['env']))
            res = [{'enlace': d['enlaceOficial'], 'estado': estado} for d in enviados]
            return subprocess.CompletedProcess(cmd, 0, stdout='RESUMEN ' + json.dumps({'publicadas': len(res), 'resultados': res}), stderr='')
        return falso

    def revisar(self, estado='publicada'):
        with mock.patch.object(aprobaciones.shutil, 'which', return_value='npx'):
            return aprobaciones.revisar(self.tg, self.cfg, HOY, self.aqui, ejecutar=self.publicador(estado))

    def test_manda_cada_curso_con_sus_botones_y_no_repite(self):
        self.assertEqual(aprobaciones.enviar_para_aprobar(self.tg, [doc(1), doc(2)], HOY, self.aqui), 2)
        self.assertEqual(aprobaciones.enviar_para_aprobar(self.tg, [doc(1)], HOY, self.aqui), 0)
        _, texto, botones = self.tg.enviados[0]
        self.assertIn('Curso virtual gratuito número 1', texto)
        self.assertEqual([b[0] for b in botones[0]], ['✅ Publicar', '❌ Descartar'])
        self.assertTrue(all(len(b[1].encode()) <= 64 for b in botones[0]), 'Telegram solo deja 64 bytes por botón')

    def test_aprobar_publica_y_descartar_olvida(self):
        aprobaciones.enviar_para_aprobar(self.tg, [doc(1), doc(2)], HOY, self.aqui)
        k1, k2 = aprobaciones.clave_de(doc(1)['enlaceOficial']), aprobaciones.clave_de(doc(2)['enlaceOficial'])
        self.tg.tocar(f'pub:{k1}')
        self.tg.tocar(f'des:{k2}')
        self.revisar()
        datos = aprobaciones.cargar(self.aqui)
        self.assertEqual(datos['cursos'][k1]['estado'], 'publicada')
        self.assertEqual(datos['cursos'][k2]['estado'], 'descartada')
        self.assertEqual([d['enlaceOficial'] for d in self.llamadas[0][0]], [doc(1)['enlaceOficial']], 'solo se publica lo aprobado')
        self.assertEqual(self.llamadas[0][1]['UNINEXO_BOT_PASSWORD'], 'secreta')
        self.assertIn('Publicado', self.tg.editados[101])
        self.assertIn('Descartado', self.tg.editados[102])
        # una segunda vuelta no vuelve a publicar ni a leer los mismos toques
        self.revisar()
        self.assertEqual(len(self.llamadas), 1)

    def test_solo_valen_los_toques_del_dueno(self):
        aprobaciones.enviar_para_aprobar(self.tg, [doc(1)], HOY, self.aqui)
        k = aprobaciones.clave_de(doc(1)['enlaceOficial'])
        self.tg.tocar(f'pub:{k}', de='999', chat='999')
        self.revisar()
        self.assertEqual(aprobaciones.cargar(self.aqui)['cursos'][k]['estado'], 'pendiente')
        self.assertEqual(self.llamadas, [])
        self.assertIn('Solo el administrador', self.tg.respuestas[0])

    def test_si_el_publicador_falla_queda_aprobado_y_se_reintenta(self):
        aprobaciones.enviar_para_aprobar(self.tg, [doc(1)], HOY, self.aqui)
        k = aprobaciones.clave_de(doc(1)['enlaceOficial'])
        self.tg.tocar(f'pub:{k}')
        caido = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 4, stdout='RESUMEN {"error": "No pude iniciar sesión"}', stderr='')
        with mock.patch.object(aprobaciones.shutil, 'which', return_value='npx'):
            aprobaciones.revisar(self.tg, self.cfg, HOY, self.aqui, ejecutar=caido)
        self.assertEqual(aprobaciones.cargar(self.aqui)['cursos'][k]['estado'], 'aprobada')
        self.assertTrue(any('No pude publicar' in t for _, t, _ in self.tg.enviados))
        self.revisar()
        self.assertEqual(aprobaciones.cargar(self.aqui)['cursos'][k]['estado'], 'publicada')

    def test_lo_que_nadie_toca_vence(self):
        aprobaciones.enviar_para_aprobar(self.tg, [doc(1)], date(2026, 10, 1), self.aqui)
        self.revisar()
        k = aprobaciones.clave_de(doc(1)['enlaceOficial'])
        self.assertEqual(aprobaciones.cargar(self.aqui)['cursos'][k]['estado'], 'vencida')
        self.assertIn('Venció', self.tg.editados[101])

    def test_si_ya_estaba_en_la_web_lo_dice(self):
        aprobaciones.enviar_para_aprobar(self.tg, [doc(1)], HOY, self.aqui)
        self.tg.tocar(f'pub:{aprobaciones.clave_de(doc(1)["enlaceOficial"])}')
        self.revisar('repetida')
        self.assertIn('Ya estaba', self.tg.editados[101])


if __name__ == '__main__':
    unittest.main()
