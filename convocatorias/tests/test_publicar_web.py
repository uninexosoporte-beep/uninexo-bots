"""Pruebas de la publicación automática de convocatorias (sin internet: el publicador se simula)."""
import json
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


class TestPublicarWebConvocatorias(unittest.TestCase):
    def setUp(self):
        self.aqui = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.aqui, 'salida'))
        for n in ['candidatas-2026-10-09.json', 'candidatas-2026-10-15.json', 'candidatas-2026-10-20.json', 'convocatorias-2026-10-20.pdf']:
            open(os.path.join(self.aqui, 'salida', n), 'w').write('[]')
        self.proyecto = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.proyecto, 'scripts'))
        open(os.path.join(self.proyecto, 'scripts', 'publicar-convocatorias-bot.ts'), 'w').write('')
        self.cred = os.path.join(self.aqui, 'cred.env')
        open(self.cred, 'w').write('UNINEXO_BOT_PASSWORD=secreta\nUNINEXO_BOT_APPCHECK_DEBUG=token\n')
        self.cfg = {'publicacion_automatica': {'activa': True, 'proyecto': self.proyecto, 'credenciales': self.cred, 'dias_archivos': 7}}

    def correr(self, salida, codigo=0):
        visto = {}

        def falso(cmd, **kw):
            visto['cmd'], visto['env'] = cmd, kw['env']
            return subprocess.CompletedProcess(cmd, codigo, stdout=salida, stderr='')
        with mock.patch.object(publicar_web.shutil, 'which', return_value='npx'):
            return publicar_web.publicar(self.cfg, self.aqui, HOY, ejecutar=falso), visto

    def test_usa_las_credenciales_del_bot_de_empleos_sin_ponerlas_en_el_comando(self):
        r, visto = self.correr('RESUMEN {"publicadas": 2, "titulosNuevos": ["Guardaparques SERNANP", "Prácticas en MARINA"]}')
        self.assertEqual(r['publicadas'], 2)
        self.assertEqual(visto['env']['UNINEXO_BOT_PASSWORD'], 'secreta')
        self.assertEqual(visto['env']['UNINEXO_BOT_APPCHECK_DEBUG'], 'token')
        self.assertNotIn('secreta', ' '.join(visto['cmd']))
        self.assertEqual([os.path.basename(a) for a in visto['cmd'][3:]], ['candidatas-2026-10-15.json', 'candidatas-2026-10-20.json'])
        self.assertIn('Publiqué 2 convocatorias', publicar_web.mensaje(r))

    def test_no_vuelve_a_publicar_los_archivos_ya_publicados(self):
        self.correr('RESUMEN {"publicadas": 2}')
        r, visto = self.correr('RESUMEN {"publicadas": 0}')
        self.assertEqual(r, {'publicadas': 0, 'nuevas': 0})
        self.assertEqual(visto, {}, 'ni siquiera llama al publicador')

    def test_si_falla_no_marca_nada_y_reintenta_mañana(self):
        r, _ = self.correr('RESUMEN {"error": "No pude iniciar sesión"}', 4)
        self.assertIn('No pude publicar', publicar_web.mensaje(r))
        self.assertFalse(os.path.exists(os.path.join(self.aqui, publicar_web.MEMORIA)))

    def test_sin_contrasena_avisa(self):
        open(self.cred, 'w').write('OTRA=1\n')
        self.assertIn('UNINEXO_BOT_PASSWORD', publicar_web.publicar(self.cfg, self.aqui, HOY)['error'])


if __name__ == '__main__':
    unittest.main()
