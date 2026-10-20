"""Pruebas de la publicación automática en la web (sin internet ni Firebase: el publicador se simula)."""
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import publicar_web  # noqa: E402

HOY = date(2026, 10, 20)
CFG = {'publicacion_automatica': {'activa': True, 'proyecto': os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dias_archivos': 7}}


class TestPublicarWeb(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for nombre in ['nuevas-2026-10-10.json', 'nuevas-2026-10-14.json', 'nuevas-2026-10-20.json', 'nuevas-2026-10-20-2.json', 'otro.json']:
            open(os.path.join(self.tmp, nombre), 'w').write('[]')
        # un «proyecto» falso con el script, para no depender de D:\uninexo
        self.proyecto = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.proyecto, 'scripts'))
        open(os.path.join(self.proyecto, 'scripts', 'publicar-empleos-bot.ts'), 'w').write('')
        self.cfg = {'publicacion_automatica': {'activa': True, 'proyecto': self.proyecto, 'dias_archivos': 7}}

    def test_toma_solo_los_archivos_de_los_ultimos_dias(self):
        r = [os.path.basename(x) for x in publicar_web.archivos_recientes(self.tmp, HOY, 7)]
        self.assertEqual(r, ['nuevas-2026-10-14.json', 'nuevas-2026-10-20-2.json', 'nuevas-2026-10-20.json'])

    def test_apagada_o_sin_contrasena(self):
        self.assertIsNone(publicar_web.publicar({'publicacion_automatica': {'activa': False}}, {}, self.tmp, HOY))
        self.assertIn('UNINEXO_BOT_PASSWORD', publicar_web.publicar(self.cfg, {}, self.tmp, HOY)['error'])

    def test_lee_el_resumen_del_publicador_y_pasa_la_clave_por_el_entorno(self):
        visto = {}

        def falso(cmd, **kw):
            visto['cmd'], visto['env'] = cmd, kw['env']
            return subprocess.CompletedProcess(cmd, 0, stdout='Firestore listo\nRESUMEN {"publicadas": 120, "yaPublicadas": 30, "conProblemas": 2}\n', stderr='')
        with mock.patch.object(publicar_web.shutil, 'which', return_value='npx'):
            r = publicar_web.publicar(self.cfg, {'UNINEXO_BOT_PASSWORD': 'secreta'}, self.tmp, HOY, ejecutar=falso)
        self.assertEqual(r['publicadas'], 120)
        self.assertEqual(visto['env']['UNINEXO_BOT_PASSWORD'], 'secreta')
        self.assertNotIn('secreta', ' '.join(visto['cmd']), 'la contraseña nunca va en la línea de comandos')
        self.assertIn('Publiqué 120 plazas', publicar_web.mensaje(r))

    def test_si_el_publicador_falla_lo_dice(self):
        falso = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 1, stdout='boom', stderr='')
        with mock.patch.object(publicar_web.shutil, 'which', return_value='npx'):
            r = publicar_web.publicar(self.cfg, {'UNINEXO_BOT_PASSWORD': 'x'}, self.tmp, HOY, ejecutar=falso)
        self.assertIn('error', r)
        self.assertIn('No pude publicar', publicar_web.mensaje(r))


if __name__ == '__main__':
    unittest.main()
