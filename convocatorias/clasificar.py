"""Convierte un título de gob.pe en una convocatoria con los campos de la pestaña «Convocatorias» de UniNexo (prácticas, voluntariado, part-time, empleo joven).

Todo se deduce de palabras del título y de la propia página (si se deja leer). Lo que no se sabe NO se inventa:
  · sin fecha en la página → sin fecha límite;
  · sin lugar en el título → «Todo el Perú».
Los procesos CAS y las plazas del Estado los cubre el bot de Empleos: aquí solo salen si lo pides en las reglas.
"""
import html
import re
import unicodedata
from datetime import date, timedelta

import gobpe

REGION_TODAS = 'Todo el Perú'
TIPOS = ['practicas', 'voluntariado', 'part_time', 'full_time', 'cas']
TIPO_ETIQUETA = {'practicas': 'Prácticas pre y profesionales', 'voluntariado': 'Voluntariados', 'part_time': 'Part-time',
                 'full_time': 'Programas de empleo y primer empleo', 'cas': 'Procesos CAS'}

# primer tipo que coincide (de más a menos específico)
TIPOS_RE = [
    ('voluntariado', r'voluntari'),
    ('part_time', r'part[- ]?time|medio tiempo|tiempo parcial'),
    ('practicas', r'practicantes?|pr[aá]cticas? (pre ?)?profesionales?|pr[aá]cticas? pre|programa de pr[aá]cticas|convocatoria de pr[aá]cticas|'
                  r'concurso (p[uú]blico )?de pr[aá]cticas|convocatoria pr[aá]cticas?\b|pr[aá]cticas? n[°º.o ]|modalidades? formativas?|pasant[ií]a|internship|\btrainee'),
    ('full_time', r'j[oó]venes profesionales|primer empleo|inserci[oó]n laboral|feria laboral|ferias laborales|programa de talento|programa de empleo|'
                  r'j[oó]venes productivos|impulsa per[uú]|trabaja per[uú]|revalora per[uú]'),
    ('cas', r'\bcas\b|proceso cas|contrataci[oó]n administrativa de servicios'),
]
# Lo que NO es una convocatoria abierta para el estudiante: resultados, listas, compras, eventos ya hechos, buenas prácticas de otro tipo…
NEGATIVO = re.compile(
    r'resultado|lista de|admitid|seleccionad|ganador|acta\b|oficio|licitaci|adjudicaci|cotizaci|subasta|adquisici|obra\b|clausur|inaugur|ceremonia|premiaci[oó]n|'
    r'entrega de|visita|reconoce|felicita|sancion|cuadro multianual|erratas|nota de prensa|comunicado|cronograma de|apoyo escolar|escolares|'
    r'buenas pr[aá]cticas|pr[aá]cticas (agr|ambient|saludable|pedag|docente|de higiene|culturales|de crianza|sostenible|de seguridad|de manufactura|de manejo)|'
    r'concluid|desierto|declara|anula|suspend|deja sin efecto|reprograma|servicio militar', re.I)
# Instituciones locales (municipios, UGEL, gobiernos regionales, hospitales…): se ignoran salvo que las pidas en las reglas
LOCALES = ('muni', 'region', 'ugel', 'drel', 'dre', 'gore', 'diresa', 'geresa', 'hospital', 'red', 'epss', 'csj', 'consulado', 'embajada', 'prefectura', 'agrorural-', 'sede')

NOMBRES = {
    'pronabec': 'PRONABEC', 'servir': 'SERVIR', 'mtpe': 'Ministerio de Trabajo (MTPE)', 'concytec': 'CONCYTEC', 'minedu': 'Ministerio de Educación', 'sencico': 'SENCICO',
    'serfor': 'SERFOR', 'inia': 'INIA', 'osiptel': 'OSIPTEL', 'sunass': 'SUNASS', 'osinergmin': 'Osinergmin', 'indecopi': 'INDECOPI', 'cultura': 'Ministerio de Cultura',
    'minam': 'Ministerio del Ambiente', 'produce': 'Ministerio de la Producción', 'minsa': 'Ministerio de Salud', 'sunedu': 'SUNEDU', 'senamhi': 'SENAMHI',
    'igp': 'Instituto Geofísico del Perú', 'inei': 'INEI', 'sunat': 'SUNAT', 'contraloria': 'Contraloría General', 'unamad': 'UNAMAD', 'midis': 'MIDIS', 'mimp': 'MIMP',
    'mef': 'MEF', 'rree': 'Cancillería', 'minjus': 'Ministerio de Justicia', 'ins': 'Instituto Nacional de Salud', 'sernanp': 'SERNANP', 'senasa': 'SENASA', 'sbs': 'SBS',
    'oefa': 'OEFA', 'ana': 'Autoridad Nacional del Agua', 'senaju': 'SENAJU', 'juventud': 'SENAJU', 'sunarp': 'SUNARP', 'essalud': 'EsSalud', 'indeci': 'INDECI',
    'ipd': 'Instituto Peruano del Deporte', 'devida': 'DEVIDA', 'sutran': 'SUTRAN', 'mincetur': 'MINCETUR', 'mtc': 'Ministerio de Transportes (MTC)', 'vivienda': 'Ministerio de Vivienda',
    'anin': 'ANIN', 'smv': 'SMV', 'pj': 'Poder Judicial', 'mpfn': 'Ministerio Público', 'reniec': 'RENIEC', 'jne': 'JNE', 'onpe': 'ONPE', 'congreso': 'Congreso de la República',
}


def sin_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def clave_texto(s):
    return re.sub(r'[^a-z0-9]+', ' ', sin_tildes(s or '').lower()).strip()


def es_local(slug):
    s = (slug or '').lower()
    return any(s.startswith(p) for p in LOCALES)


def nombre_institucion(slug):
    return NOMBRES.get(slug) or (slug or '').upper().replace('-', ' ')


def tipo_de(titulo):
    t = sin_tildes(titulo or '').lower()
    for tipo, patron in TIPOS_RE:
        if re.search(sin_tildes(patron), t):
            return tipo
    return None


def fecha_pasada_en_titulo(titulo, hoy):
    """Títulos como «Jornada de voluntariado 28/08/2026» con una fecha ya vencida: es un evento que pasó."""
    for d, m, a in re.findall(r'(\d{1,2})/(\d{1,2})/(20\d\d)', titulo or ''):
        try:
            if date(int(a), int(m), int(d)) < hoy:
                return True
        except ValueError:
            pass
    return False


# Una NOTICIA solo cuenta si su título invita a hacer algo (convoca, abre inscripciones…): «Estudiantes participan en una pasantía» es un hecho pasado, no una convocatoria
SENAL_CONVOCATORIA = re.compile(r'convoca|convocatoria|inscrip|postul|\babre\b|\babren\b|abierta|lanza\b|lanzan\b|invita|ya puedes|plazo|vacantes|cupos|\bparticipa\b|\bparticipar\b|se parte|unete', re.I)


def es_oportunidad(titulo, hoy=None, fuente=None):
    """¿Parece una convocatoria de prácticas, voluntariado o empleo joven (y no un resultado, una nota de prensa o un evento ya hecho)?
    `fuente` = de dónde salió el título: las noticias (gobpe-noticias) piden además una señal de convocatoria en el título."""
    if tipo_de(titulo) is None or NEGATIVO.search(titulo or ''):
        return False
    if fuente == 'gobpe-noticias' and not SENAL_CONVOCATORIA.search(sin_tildes(titulo or '')):
        return False
    return not (hoy and fecha_pasada_en_titulo(titulo, hoy))


def region_de(texto):
    """Región del Perú mencionada en el texto; por defecto, todo el Perú."""
    t = sin_tildes(texto or '').lower()
    for r in ['Madre de Dios', 'La Libertad', 'San Martín', 'Amazonas', 'Áncash', 'Apurímac', 'Arequipa', 'Ayacucho', 'Cajamarca', 'Callao', 'Cusco', 'Huancavelica', 'Huánuco',
              'Junín', 'Lambayeque', 'Lima', 'Loreto', 'Moquegua', 'Pasco', 'Piura', 'Puno', 'Tacna', 'Tumbes', 'Ucayali']:
        if re.search(r'\b' + re.escape(sin_tildes(r).lower()) + r'\b', t):
            return r
    return REGION_TODAS


# ------------------------------------------------------------------ lectura de la página de la convocatoria
CLAVE_FECHA = r'(?:hasta|plazo|cierre|inscripci|postulaci|vence|l[ií]mite|recepci[oó]n|registro)'
FECHA_TEXTO = re.compile(r'(\d{1,2})\s+de\s+([a-záéíóú]+)(?:\s+de\s+(20\d\d))?', re.I)
FECHA_NUM = re.compile(r'(\d{1,2})[/-](\d{1,2})[/-](20\d\d)')


def _texto_pagina(t):
    t = re.sub(r'<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', t, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t))).strip()


def fechas_clave(texto, hoy):
    """Fechas FUTURAS que aparecen cerca de «hasta / plazo / cierre / inscripciones / postulación»."""
    encontradas = set()
    for m in re.finditer(CLAVE_FECHA, texto, re.I):
        trozo = texto[m.start(): m.start() + 130]
        for d, mes, anio in FECHA_TEXTO.findall(trozo):
            mm = gobpe.MESES.get(sin_tildes(mes).lower())
            if mm:
                a = int(anio) if anio else (hoy.year if mm >= hoy.month else hoy.year + 1)
                encontradas.add((a, mm, int(d)))
        for d, mm, a in FECHA_NUM.findall(trozo):
            encontradas.add((int(a), int(mm), int(d)))
    futuras = []
    for a, mm, d in encontradas:
        try:
            f = date(a, mm, d)
        except ValueError:
            continue
        if hoy <= f <= hoy + timedelta(days=270):  # una «fecha límite» a más de 9 meses casi nunca lo es (suele ser el fin del programa)
            futuras.append(f)
    return sorted(futuras)


def leer_pagina(url, hoy):
    """Datos extra de la página de la convocatoria. Devuelve {} si no se pudo leer (no pasa nada: se usa solo el título)."""
    try:
        return analizar_pagina(gobpe.descargar(url), hoy)
    except Exception:
        return {}


def analizar_pagina(t, hoy):
    """Del HTML de la página: descripción, fecha límite y modalidad. Solo lo que la página dice."""
    texto = _texto_pagina(t)
    desc = re.search(r'<meta[^>]+(?:property="og:description"|name="description")[^>]+content="([^"]{20,600})"', t, re.I)
    descripcion = html.unescape(desc.group(1)).strip() if desc else texto[:300]
    datos = {'descripcion': re.sub(r'\s+', ' ', descripcion)[:400]}
    fechas = fechas_clave(texto, hoy)
    if fechas:
        datos['fechaLimite'] = fechas[0].isoformat()
    mod_v, mod_p = re.search(r'virtual|en l[ií]nea|online|a distancia|remot', texto, re.I), re.search(r'presencial', texto, re.I)
    if mod_v and mod_p:
        datos['modalidad'] = 'hibrido'
    elif mod_v:
        datos['modalidad'] = 'virtual'
    elif mod_p:
        datos['modalidad'] = 'presencial'
    return datos
