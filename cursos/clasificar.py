"""Convierte un título de gob.pe en una oportunidad con los campos de la sección Cursos de UniNexo.

Todo se deduce de palabras del título y de la propia página (si se deja leer). Lo que no se sabe NO se inventa:
  · costo sin confirmar → «Por confirmar» (la sección ya lo muestra como «Costo por confirmar»);
  · sin fecha en la página → sin fecha límite.
"""
import html
import re
import unicodedata
from datetime import date, timedelta

import gobpe

AREA_TODAS = 'Todas las carreras'
COSTO_POR_CONFIRMAR = 'Por confirmar'
TIPOS = ['curso', 'diplomado', 'especializacion', 'certificacion', 'taller', 'webinar', 'beca', 'convocatoria', 'experiencia_laboral', 'voluntariado']
TIPO_ETIQUETA = {'beca': 'Becas', 'especializacion': 'Especializaciones y programas de extensión', 'diplomado': 'Diplomados', 'curso': 'Cursos y capacitaciones',
                 'certificacion': 'Certificaciones', 'taller': 'Talleres', 'webinar': 'Webinars y charlas', 'voluntariado': 'Voluntariados',
                 'experiencia_laboral': 'Pasantías y experiencia', 'convocatoria': 'Concursos y convocatorias'}

# primer tipo que coincide (de más a menos específico)
TIPOS_RE = [
    ('beca', r'\bbecas?\b|scholarship'),
    ('especializacion', r'especializaci|maestr[ií]a|posgrado|programa de extensi[oó]n|\bpeu\b'),
    ('diplomado', r'diplomado'),
    ('certificacion', r'certificaci[oó]n'),
    ('voluntariado', r'voluntari'),
    ('experiencia_laboral', r'pasant[ií]a|internship'),
    ('taller', r'taller'),
    ('webinar', r'webinar|seminario web|conversatorio|charla|conferencia|foro '),
    ('curso', r'\bcursos?\b|capacitaci[oó]n|mooc|escuela de|\baprende|\bformaci[oó]n'),
    # concursos y premios solo si hablan de estudio, investigación o jóvenes (no el «Concurso Nacional del Pisco»)
    ('convocatoria', r'(concurso|fondo concursable|olimpiada|hackat[oó]n)(?=.*(investigaci|ensayo|innovaci|ciencia|tecnolog|estudiante|j[oó]venes|universitari|emprend|proyecto|beca))'),
    # los premios casi siempre son para investigadores o profesionales: solo si el título habla de estudiantes o jóvenes
    ('convocatoria', r'premio(?=.*(estudiant|universitari|j[oó]venes|tesis))'),
]
# Lo que NO es una oportunidad de estudio para el estudiante: personal (eso es de Empleos), compras, resultados, noticias de eventos ya hechos…
NEGATIVO = re.compile(
    r'\bcas\b|proceso cas|contrataci[oó]n|plaza|pr[aá]cticas (pre)?profesionales|convocatoria n|resultado|lista de|admitid|seleccionad|ganador|acta\b|oficio|'
    r'contrato|licitaci|adjudicaci|cotizaci|subasta|adquisici|obra\b|clausur|inaugur|ceremonia|premiaci[oó]n|entrega de|visita|reconoce|felicita|sancion|'
    r'cuadro multianual|erratas|nota de prensa|comunicado|cronograma de|apoyo escolar|docentes?\b|directiv|escolares', re.I)
# Notas de prensa que cuentan algo que YA pasó o que solo informa (20/10/2026: de 50 candidatas en 8 días, ~40 eran esto):
# «Hospital … realizó taller», «Más de 100 voluntarios participaron», «Sunedu fortalece…», «SIS obtiene certificación»…
NOTICIA = re.compile(
    r'\b(realiz(a|o|aron|amos)|culmin|participaron|particip[oó]\b|fortalec(e|en|io|imos)\b|impuls(a|an|o)\b|obtien|obtuvo|conquist|accedieron|'
    r'fueron|inici[oó]\b|lider[oó]|abordan|coordina|brind(a|an|o)\b|recomienda|reunir[aá]|ganaron|logr[oó]|permite|aprende(n)? a\b|aprenden\b|aprender[aá]n|'
    r'capacit(o|aron)\b|se capacitan|clausur|entreg[oó]|celebr|destac)', re.I)
# Para quién es: si el título ya dice que es para personal, trabajadores o beneficiarios de un programa, no es para el estudiante
SOLO_PERSONAL_TITULO = re.compile(
    r'(dirigid[oa]s? a|para) (los |las |sus |el |la )?(beneficiari|personal|servidor|funcionari|trabajador|productor|profesionales de la salud|internos|pensionist|serumistas)|'
    r'\ba (los |las |sus )?(trabajadores|servidores|funcionarios|profesionales)\b', re.I)
# Instituciones locales (municipios, UGEL, gobiernos regionales, hospitales…): se ignoran salvo que las pidas en las reglas
LOCALES = ('muni', 'region', 'ugel', 'drel', 'dre', 'gore', 'diresa', 'geresa', 'hospital', 'red', 'epss', 'csj', 'consulado', 'embajada', 'prefectura', 'agrorural-', 'sede',
           # hospitales nacionales (sus capacitaciones son para su personal): hnch, hnseb, hma, hlev…
           'hn', 'hma', 'hlev', 'hosp', 'hrd', 'insn', 'inr')

AREAS_RE = [
    ('Idiomas', r'ingl[eé]s|idioma|franc[eé]s|alem[aá]n|portugu[eé]s|quechua|aimara|lengua'),
    ('Salud', r'salud|m[eé]dic|enfermer|obstetr|nutrici|farmac|epidemiolog|cl[ií]nic|hospital|donaci[oó]n|bioseguridad'),
    ('Psicología', r'psicolog|salud mental'),
    ('Derecho y Ciencias Políticas', r'derecho|jur[ií]dic|legal|justicia|notari|constituci[oó]n|derechos humanos'),
    ('Contabilidad y Finanzas', r'contab|financ|tribut|auditor[ií]a|presupuesto'),
    ('Economía', r'econom|inversi[oó]n'),
    ('Gestión Pública', r'gesti[oó]n p[uú]blica|servicio civil|contrataciones del estado|control gubernamental|administraci[oó]n p[uú]blica|invierte|funci[oó]n p[uú]blica|servidores p[uú]blicos'),
    ('Educación', r'educaci[oó]n|pedag|ense[nñ]anza|did[aá]ctic'),
    ('Tecnología e Informática', r'inform[aá]tic|tecnolog|program|software|datos|inteligencia artificial|ciberseg|digital|sistemas|\bia\b'),
    ('Arquitectura y Construcción', r'construcci|arquitect|edificaci|saneamiento|sencico|civil'),
    ('Agropecuaria y Ambiente', r'agr[oí]|ambient|forestal|cacao|caf[eé]\b|cuy|ap[ií]col|palto|ganader|pecuari|biodivers|cambio clim|reciclaje|residuos'),
    ('Ingeniería', r'ingenier|el[eé]ctric|mec[aá]nic|industrial|miner|petr[oó]leo|energ[ií]a'),
    ('Comunicación y Marketing', r'comunicaci[oó]n|period|marketing|redes sociales|publicidad'),
    ('Turismo y Hotelería', r'turism|hoteler|gastronom'),
    ('Arte y Diseño', r'\barte\b|dise[nñ]o|m[uú]sica|danza|teatro|audiovisual|cine\b|artesan'),
    ('Ciencias Sociales y Humanidades', r'sociolog|antropolog|historia|cultura|human|patrimonio'),
    ('Ciencias Básicas', r'matem[aá]tic|f[ií]sica|qu[ií]mica|biolog|ciencia|investigaci[oó]n|innovaci[oó]n'),
    ('Empleabilidad y Desarrollo Personal', r'empleo|empleabilidad|emprend|liderazgo|habilidades|vocacional|carrera profesional'),
    ('Administración y Negocios', r'administraci[oó]n|negocios|empresa|gesti[oó]n|gerencia'),
]
NOMBRES = {
    'pronabec': 'PRONABEC', 'servir': 'SERVIR', 'mtpe': 'Ministerio de Trabajo (MTPE)', 'concytec': 'CONCYTEC', 'minedu': 'Ministerio de Educación', 'sencico': 'SENCICO',
    'serfor': 'SERFOR', 'inia': 'INIA', 'osiptel': 'OSIPTEL', 'sunass': 'SUNASS', 'osinergmin': 'Osinergmin', 'indecopi': 'INDECOPI', 'cultura': 'Ministerio de Cultura',
    'minam': 'Ministerio del Ambiente', 'produce': 'Ministerio de la Producción', 'minsa': 'Ministerio de Salud', 'ensap': 'Escuela Nacional de Salud Pública',
    'sunedu': 'SUNEDU', 'senamhi': 'SENAMHI', 'igp': 'Instituto Geofísico del Perú', 'inei': 'INEI', 'sunat': 'SUNAT', 'contraloria': 'Contraloría General',
    'unamad': 'UNAMAD', 'midis': 'MIDIS', 'mimp': 'MIMP', 'mef': 'MEF', 'rree': 'Cancillería', 'minjus': 'Ministerio de Justicia', 'ins': 'Instituto Nacional de Salud',
    'inictel-uni': 'INICTEL-UNI', 'sernanp': 'SERNANP', 'senasa': 'SENASA', 'sbs': 'SBS', 'oefa': 'OEFA', 'ana': 'Autoridad Nacional del Agua', 'juventud': 'SENAJU',
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
    """Títulos como «Capacitación Virtual 28/08/2026» o «…este jueves 15 de octubre» con una fecha ya vencida: es un evento que pasó."""
    fechas = [(int(a), int(m), int(d)) for d, m, a in re.findall(r'(\d{1,2})/(\d{1,2})/(20\d\d)', titulo or '')]
    for d, mes, anio in re.findall(r'(\d{1,2})\s+de\s+([a-záéíóú]+)(?:\s+(?:de|del)\s+(20\d\d))?', titulo or '', re.I):
        mm = gobpe.MESES.get(sin_tildes(mes).lower())
        if mm:
            fechas.append((int(anio) if anio else hoy.year, mm, int(d)))
    for a, m, d in fechas:
        try:
            if date(a, m, d) < hoy:
                return True
        except ValueError:
            pass
    return False


def es_oportunidad(titulo, hoy=None):
    """¿Parece una beca, curso, programa o convocatoria de estudio (y no una plaza, un resultado o una nota de prensa)?"""
    if tipo_de(titulo) is None or NEGATIVO.search(titulo or '') or NOTICIA.search(sin_tildes(titulo or '')) or SOLO_PERSONAL_TITULO.search(sin_tildes(titulo or '')):
        return False
    return not (hoy and fecha_pasada_en_titulo(titulo, hoy))


def area_de(texto):
    t = sin_tildes(texto or '').lower()
    for area, patron in AREAS_RE:
        if re.search(sin_tildes(patron), t):
            return area
    return AREA_TODAS


def region_de(texto):
    """Región del Perú mencionada en el texto (para cursos regionales); por defecto, todo el país."""
    t = sin_tildes(texto or '').lower()
    for r in ['Madre de Dios', 'La Libertad', 'San Martín', 'Amazonas', 'Áncash', 'Apurímac', 'Arequipa', 'Ayacucho', 'Cajamarca', 'Callao', 'Cusco', 'Huancavelica', 'Huánuco',
              'Ica', 'Junín', 'Lambayeque', 'Lima', 'Loreto', 'Moquegua', 'Pasco', 'Piura', 'Puno', 'Tacna', 'Tumbes', 'Ucayali']:
        if re.search(r'\b' + re.escape(sin_tildes(r).lower()) + r'\b', t) and r not in ('Ica',):
            return r
    return 'Todo el país'


# ------------------------------------------------------------------ lectura de la página de la oportunidad
GRATIS = re.compile(r'gratuit[oa]s?|gratis|sin costo|sin cargo|no tiene costo|no tiene ning[uú]n costo|beca completa|cubre (el )?100|financiad[oa] (al 100|por)', re.I)
COSTO = re.compile(r'(?:costo|inversi[oó]n|derecho de inscripci[oó]n|matr[ií]cula|cuota|pago)[^.\n]{0,40}?S/\.?\s?(\d{2,5}(?:[.,]\d{2})?)', re.I)
CLAVE_FECHA = r'(?:hasta|plazo|cierre|inscripci|postulaci|vence|l[ií]mite|recepci[oó]n|registro)'
FECHA_TEXTO = re.compile(r'(\d{1,2})\s+de\s+([a-záéíóú]+)(?:\s+de\s+(20\d\d))?', re.I)
# La página dice que es SOLO para personal de una entidad (y no invita a estudiantes ni a la ciudadanía)
SOLO_PERSONAL = re.compile(
    r'dirigid[oa]s?\s*(?:a|al|:)\s*:?\s*(?:los |las |el |la |sus )?(?:personal|funcionari|servidor|trabajador|profesionales de la salud|m[eé]dicos|docentes|productor|beneficiari|serums)|'
    r'v[ií]nculo laboral|nombramiento o contrato|oficio[^.]{0,80}entidad|acredite para participar', re.I)
ABIERTO = re.compile(r'estudiant|universitari|egresad|ciudadan|p[uú]blico en general|comunidad acad[eé]mica|personas interesadas|j[oó]venes', re.I)
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
    """Datos extra de la página de la oportunidad. Devuelve {} si no se pudo leer (no pasa nada: se usa solo el título)."""
    try:
        return analizar_pagina(gobpe.descargar(url), hoy)
    except Exception:
        return {}


def analizar_pagina(t, hoy):
    """Del HTML de la página: descripción, si dice que es gratis (o su costo), fecha límite y modalidad. Solo lo que la página dice."""
    texto = _texto_pagina(t)
    desc = re.search(r'<meta[^>]+(?:property="og:description"|name="description")[^>]+content="([^"]{20,600})"', t, re.I)
    descripcion = html.unescape(desc.group(1)).strip() if desc else texto[:300]
    datos = {'descripcion': re.sub(r'\s+', ' ', descripcion)[:400]}
    m = SOLO_PERSONAL.search(texto)
    if m and not ABIERTO.search(texto[max(0, m.start() - 40): m.end() + 250]):
        datos['soloPersonal'] = True
    todo = descripcion + ' ' + texto  # la descripción de la página (meta) suele decir «gratuito» aunque el cuerpo no lo repita
    if GRATIS.search(todo):
        datos['gratuito'] = True
    else:
        m = COSTO.search(todo)
        if m:
            datos['gratuito'] = False
            datos['costo'] = f'S/ {m.group(1)}'
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
