"""Reglas del bot de Cursos y Oportunidades (se ajustan en config.json → "reglas").

· tipos / areas: `solo` (vacío = todos) e `ignorar`. Los tipos y áreas son los de la sección Cursos de UniNexo.
· solo_gratuitos: avisa solo de lo que su página dice que es gratis; `incluir_costo_desconocido` decide qué pasa con lo que no lo dice.
· dias_minimos_abierta: si la página trae fecha límite, cuántos días de margen debe tener.
· instituciones: `incluir` (se leen y avisan aunque sean locales, ej. «unamad») e `ignorar`; `incluir_locales` abre municipios, UGEL, regiones…
· palabras_excluir: nunca avisar un título que las tenga.
"""
from datetime import date, timedelta

from clasificar import AREA_TODAS, TIPOS, clave_texto, es_local


def _conjunto(lista):
    return {clave_texto(x) for x in (lista or [])}


def reglas(cfg):
    return (cfg or {}).get('reglas') or {}


def institucion_permitida(slug, cfg):
    r = reglas(cfg)
    inst = r.get('instituciones') or {}
    s = clave_texto(slug)
    if s in _conjunto(inst.get('ignorar')):
        return False
    if s in _conjunto(inst.get('incluir')):
        return True
    return bool(r.get('incluir_locales', False)) or not es_local(slug)


def evaluar(c, cfg, hoy):
    """Motivo por el que NO se avisa esta oportunidad (None = sirve). `c` = candidato con tipo, area, slug, nombre, gratuito, fechaLimite."""
    r = reglas(cfg)
    if not institucion_permitida(c['slug'], cfg):
        return 'institución local o ignorada'
    titulo = clave_texto(c['name'])
    for palabra in r.get('palabras_excluir') or []:
        if clave_texto(palabra) and clave_texto(palabra) in titulo:
            return f'título excluido por tu regla ({palabra})'
    tipos = r.get('tipos') or {}
    solo_t, ign_t = _conjunto(tipos.get('solo')), _conjunto(tipos.get('ignorar'))
    if solo_t and clave_texto(c['tipo']) not in solo_t:
        return 'otro tipo (no está en tu lista)'
    if clave_texto(c['tipo']) in ign_t:
        return 'tipo ignorado por tu regla'
    areas = r.get('areas') or {}
    solo_a, ign_a = _conjunto(areas.get('solo')), _conjunto(areas.get('ignorar'))
    a = clave_texto(c['area'])
    if solo_a and a != clave_texto(AREA_TODAS) and a not in solo_a:
        return 'otra área (no está en tu lista)'
    if a in ign_a:
        return 'área ignorada por tu regla'
    if r.get('solo_gratuitos'):
        if c.get('gratuito') is False:
            return 'de pago'
        if c.get('gratuito') is None and not r.get('incluir_costo_desconocido', True):
            return 'no dice si es gratis'
    if c.get('fechaLimite'):
        minimo = hoy + timedelta(days=int(r.get('dias_minimos_abierta', 2)))
        if date.fromisoformat(c['fechaLimite']) < minimo:
            return 'cierra muy pronto o ya cerró'
    return None


def tipos_disponibles():
    return list(TIPOS)
