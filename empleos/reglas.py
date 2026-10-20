"""Reglas por REGIÓN y por CARRERA (se ajustan en config.json → "reglas").

· Región: `solo` (vacío = todas), `ignorar`, `prioritarias` (salen primero y con ⭐) y `tope_propio` (más o menos plazas que el tope general).
· Carrera: el bot deduce la carrera de cada plaza por las palabras de su cargo (catálogo CARRERAS). Con `solo` filtra; si `solo` está
  vacío solo ETIQUETA («🎓 Derecho») sin descartar nada. `incluir_sin_carrera` decide qué pasa con los cargos que no se reconocen
  (ej. «Especialista III»): por defecto SÍ pasan, para no perder plazas por un cargo ambiguo.
· Cargos: `excluir_palabras` (nunca avisar si el cargo las tiene) e `incluir_palabras` (siempre dejar pasar).
Los nombres de carrera son los mismos que usa la app en el campo «carrera» de cada plaza.
"""
import re

from normalizar import clave_texto, sin_tildes

# carrera → palabras del cargo (sin tildes, en minúsculas). Una plaza puede caer en varias carreras.
CARRERAS = {
    'Derecho': r'abogad|legal|juridic|procurador|procuradur|fiscal(?!iz)|judicial|juzgado|jurisdiccional|notari|conciliador|registrador|registral|patrocinador|defensor|sancionador|disciplinari|despacho de control|contratos y convenios',
    'Contabilidad': r'contab|contador|tesorer|presupuest|auditor|control patrimonial|costos|rentas|tributar|cajer|auxiliar de caja|responsable de caja',
    'Economía': r'econom|inversion|inversiones|formulador|evaluador de proyectos|planeamiento|planificador|planificacion',
    'Administración': r'administra|gestor|logistic|abastecimiento|contrataciones|adquisiciones|recursos humanos|personal|escalaf|planilla|remuneraci|racionaliz|organizacional|'
                      r'coordinador|jefe|responsable|secretari|almacen|archivo|tramite documentario|mesa de partes|digitador|atencion al usuario|apoyo administrativo|supervisor|gerente|gerencia|director|documental',
    'Educación': r'docente|educacion|pedag|profesor|escolar|educativ|formador|tutor|aprendizaje|convivencia|residencia estudiantil|inclusiv|auxiliar academic|director[a/]* academic|colegio de alto rendimiento',
    'Medicina': r'medic|cirujano(?! dentista)|oftalm|pediatr|ginec|anestesi|cardiol|traumat|neonat|intensiv|internista',
    'Enfermería': r'enferm',
    'Obstetricia': r'obstetr|partera',
    'Odontología': r'odont|dentista|estomatol',
    'Nutrición': r'nutri',
    'Psicología': r'psicolog',
    'Trabajo Social': r'trabajador[a/]* social|trabajo social|gestor social|asistente social|promotor|bienestar social|bienestar estudiantil|bienestar',
    'Farmacia y Química': r'farmac|quimic|bioquimic|medicamento',
    'Tecnología Médica': r'tecnolog[oa]s? medic|radiolog|terapia|terapeut|fisioterap|rehabilitaci|tecnico en laboratorio|laboratorio clinico',
    'Biología': r'biolog|microbiolog|genetic|laboratorio',
    'Ing. de Sistemas': r'sistemas|informatic|soporte (tecnico|tecnologico)|programador|desarrollador|software|base de datos|redes|ciberseg|seguridad de la informaci|'
                        r'tecnolog\w* de la informaci|\btic\b|innovacion|transformacion digital|gobierno digital|plataforma|digitalizaci|teledeteccion|\bsig\b|siagie|tecnologico',
    'Ing. Civil': r'civil|arquitect|obras|infraestructura|topogr|estructura|saneamiento|edificaci|proyectista|catastro|cartogr|urbanismo|habilitacion urbana|expediente tecnico|residente',
    'Ing. Ambiental': r'ambiental|ecosistem|recursos naturales|residuos solidos|cambio climatico|conservacion|ordenamiento territorial|areas naturales',
    'Ing. Forestal': r'forestal|silvic|fauna',
    'Agronomía y Veterinaria': r'agronom|agrari|agropecuari|agricol|zootecn|veterinar|pecuari|agroindustr|sanidad animal',
    'Ing. Industrial / Eléctrica / Minas': r'industrial|mecanic|electric|electronic|minas|minero|metalurg|petroleo|energetic|hidrocarburo',
    'Ciencias de la Comunicación': r'comunicacion|comunicador|periodis|prensa|difusion|imagen institucional|disenador|audiovisual|redes sociales|relaciones publicas|protocolo|publicidad|marketing',
    'Turismo y Hotelería': r'turism|hotel|gastronom|guia oficial|artesan',
    'Estadística': r'estadistic|matematic|econometr|\bdatos\b|siagie|indicadores',
    'Antropología, Sociología y Arqueología': r'antropol|sociolog|arqueolog|historiador|politolog|ciencias politicas|intercultural|patrimonio cultural|etnolog|gestor cultural',
    'Gestión de Riesgos y Seguridad': r'riesgo de desastres|riesgos de desastres|defensa civil|seguridad y salud en el trabajo|ssoma|prevencion',
}
CARRERAS_RE = {nombre: re.compile(patron) for nombre, patron in CARRERAS.items()}


def carreras_de(*textos):
    """Carreras a las que corresponde un cargo (lista, en el orden del catálogo)."""
    t = sin_tildes(' '.join(x for x in textos if x)).lower()
    return [nombre for nombre, rx in CARRERAS_RE.items() if rx.search(t)]


def _conjunto(lista):
    return {clave_texto(x) for x in (lista or [])}


def reglas(cfg):
    return (cfg or {}).get('reglas') or {}


# ---------------------------------------------------------------- regiones
def region_permitida(region, cfg):
    reg = reglas(cfg).get('regiones') or {}
    solo, ignorar = _conjunto(reg.get('solo')), _conjunto(reg.get('ignorar'))
    k = clave_texto(region)
    if solo and k not in solo:
        return False
    return k not in ignorar


def es_prioritaria(region, cfg):
    return clave_texto(region) in _conjunto((reglas(cfg).get('regiones') or {}).get('prioritarias'))


def tope_region(region, cfg):
    """Cuántas plazas como máximo se avisan de esa región por día."""
    propios = (reglas(cfg).get('regiones') or {}).get('tope_propio') or {}
    for k, v in propios.items():
        if clave_texto(k) == clave_texto(region):
            return int(v)
    return int(cfg['filtros']['max_por_region'])


def orden_regiones(regiones, cfg):
    """Prioritarias primero; el resto por orden alfabético."""
    return sorted(regiones, key=lambda r: (not es_prioritaria(r, cfg), clave_texto(r)))


# ---------------------------------------------------------------- cargos y carreras
def evaluar_texto(texto, carreras, cfg):
    """Motivo por el que NO se avisa un cargo según las reglas de cargos y carreras (None = pasa)."""
    r = reglas(cfg)
    cargos = r.get('cargos') or {}
    car = r.get('carreras') or {}
    t = clave_texto(texto)
    for palabra in cargos.get('excluir_palabras') or []:
        if clave_texto(palabra) and clave_texto(palabra) in t:
            return f'cargo excluido por tu regla ({palabra})'
    incluir = any(clave_texto(p) and clave_texto(p) in t for p in (cargos.get('incluir_palabras') or []))
    detectadas = _conjunto(carreras)
    ignorar, solo = _conjunto(car.get('ignorar')), _conjunto(car.get('solo'))
    if ignorar and detectadas and detectadas <= ignorar and not incluir:
        return 'carrera ignorada por tu regla'
    if solo and not incluir:
        if detectadas:
            if not (detectadas & solo):
                return 'otra carrera (no está en tu lista)'
        elif not car.get('incluir_sin_carrera', True):
            return 'sin carrera reconocida'
    return None


def evaluar(rec, cfg):
    """Reglas de región, cargo y carrera para una plaza ya convertida."""
    if not region_permitida(rec['region'], cfg):
        return 'región fuera de tu lista'
    return evaluar_texto(rec['cargo'], rec.get('carreras', []), cfg)


def etiqueta_carreras(carreras, maximo=2):
    return ', '.join(carreras[:maximo])
