"""Memoria del bot (SQLite, un solo archivo en tu PC): qué ofertas ya avisó, qué enlaces ya vio y cómo estaban las páginas vigiladas."""
import json
import sqlite3
from contextlib import closing

ESQUEMA = '''
CREATE TABLE IF NOT EXISTS ofertas (
    clave_base TEXT PRIMARY KEY,   -- región | entidad | cargo | número de convocatoria | ubicación (sin la fecha de cierre)
    fuente TEXT, region TEXT, titulo TEXT, cierre TEXT, primera_vez TEXT, avisada INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS enlaces (
    url TEXT PRIMARY KEY, fuente TEXT, titulo TEXT, fecha TEXT, primera_vez TEXT
);
CREATE TABLE IF NOT EXISTS paginas (
    id TEXT PRIMARY KEY, lineas TEXT, ultima TEXT, error_avisado INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
'''


class Almacen:
    def __init__(self, ruta):
        self.con = sqlite3.connect(ruta)
        self.con.row_factory = sqlite3.Row
        with self.con:
            self.con.executescript(ESQUEMA)

    def cerrar(self):
        self.con.close()

    # --- meta ---
    def meta(self, k, defecto=None):
        fila = self.con.execute('SELECT v FROM meta WHERE k=?', (k,)).fetchone()
        return fila['v'] if fila else defecto

    def poner_meta(self, k, v):
        with self.con:
            self.con.execute('INSERT INTO meta(k, v) VALUES(?, ?) ON CONFLICT(k) DO UPDATE SET v=excluded.v', (k, str(v)))

    def es_primera_vez(self):
        return self.meta('base_inicial') is None

    # --- ofertas de SERVIR ---
    def cierre_guardado(self, clave_base):
        fila = self.con.execute('SELECT cierre FROM ofertas WHERE clave_base=?', (clave_base,)).fetchone()
        return fila['cierre'] if fila else None

    def guardar_oferta(self, clave_base, fuente, region, titulo, cierre, hoy, avisada=1):
        with self.con:
            self.con.execute(
                'INSERT INTO ofertas(clave_base, fuente, region, titulo, cierre, primera_vez, avisada) VALUES(?,?,?,?,?,?,?) '
                'ON CONFLICT(clave_base) DO UPDATE SET cierre=excluded.cierre, avisada=MAX(avisada, excluded.avisada)',
                (clave_base, fuente, region, titulo, cierre, hoy, avisada))

    def contar_ofertas(self):
        return self.con.execute('SELECT COUNT(*) AS n FROM ofertas').fetchone()['n']

    # --- enlaces de gob.pe ---
    def enlace_visto(self, url):
        return self.con.execute('SELECT 1 FROM enlaces WHERE url=?', (url,)).fetchone() is not None

    def guardar_enlace(self, url, fuente, titulo, fecha, hoy):
        with self.con:
            self.con.execute('INSERT OR IGNORE INTO enlaces(url, fuente, titulo, fecha, primera_vez) VALUES(?,?,?,?,?)', (url, fuente, titulo, fecha, hoy))

    def contar_enlaces(self):
        return self.con.execute('SELECT COUNT(*) AS n FROM enlaces').fetchone()['n']

    # --- páginas vigiladas ---
    def pagina(self, id_):
        fila = self.con.execute('SELECT lineas, ultima, error_avisado FROM paginas WHERE id=?', (id_,)).fetchone()
        if not fila:
            return None
        return {'lineas': json.loads(fila['lineas']) if fila['lineas'] else [], 'ultima': fila['ultima'], 'error_avisado': bool(fila['error_avisado'])}

    def guardar_pagina(self, id_, lineas, hoy, error_avisado=0):
        with self.con:
            self.con.execute(
                'INSERT INTO paginas(id, lineas, ultima, error_avisado) VALUES(?,?,?,?) '
                'ON CONFLICT(id) DO UPDATE SET lineas=excluded.lineas, ultima=excluded.ultima, error_avisado=excluded.error_avisado',
                (id_, json.dumps(lineas, ensure_ascii=False), hoy, error_avisado))

    def marcar_error_pagina(self, id_, hoy):
        with self.con:
            self.con.execute(
                'INSERT INTO paginas(id, lineas, ultima, error_avisado) VALUES(?,?,?,1) '
                'ON CONFLICT(id) DO UPDATE SET error_avisado=1', (id_, '[]', hoy))
