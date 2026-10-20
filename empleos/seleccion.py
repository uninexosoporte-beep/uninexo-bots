"""De la oferta cruda del portal al registro limpio: filtros (labor manual, sueldo, régimen, fechas), elección de las 10 mejores
por región y documento listo para UniNexo (mismo formato que `convocatoriasDeServir` de la app)."""
import hashlib
import re
from datetime import date, timedelta

import reglas
from normalizar import (MANUAL, OMITIR_CARGO, cargo_final, clave_texto, departamento_desde_ubicacion, distrito_final, entidad_final,
                        fecha_iso, propios_departamentos, sin_tildes, slug, sueldo_num)

URL_SERVIR_OFERTAS = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/ofertas_laborales.xhtml'
URL_SERVIR_PRACTICAS = 'https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/modalidades_formativas.xhtml'
FUENTE_TEXTO = 'Talento Perú (SERVIR)'
PROPIOS = propios_departamentos()


def nombre_servir(departamento):
    """Cómo aparece la región en la lista «Ubicación» de SERVIR: mayúsculas y sin tildes."""
    return sin_tildes(departamento).upper().strip()


def clave_base(region, entidad_raw, cargo_raw, numero, ubicacion):
    """Identificador de una oferta: no incluye la fecha de cierre, para detectar ampliaciones."""
    texto = '|'.join([region, entidad_raw, cargo_raw, numero, ubicacion])
    return hashlib.sha1(texto.encode('utf-8')).hexdigest()[:20]


def tipo_desde_numero(numero):
    if numero.startswith('D.LEG 1057'):
        return 'CAS'
    if numero.startswith('728'):
        return 'Contrato'
    return None


def convertir(raw, fuente, region_servir=None):
    """Oferta cruda → registro. Devuelve None si no se puede ubicar la región."""
    es_practica = fuente == 'servir-practicas'
    departamento, distrito_raw = departamento_desde_ubicacion(raw.get('ubicacion'))
    region = region_servir or departamento
    if not region:
        return None
    if region_servir and departamento and departamento != region_servir:
        region = departamento  # el portal manda
    numero = (raw.get('numero') or '').strip()
    cierre = fecha_iso(raw.get('fin'))
    vacantes = int(raw['vacantes']) if str(raw.get('vacantes', '')).strip().isdigit() else 1
    sueldo = None if es_practica else sueldo_num(raw.get('remuneracion'))
    cargo = cargo_final(raw.get('cargo', ''), PROPIOS)
    return {
        'fuente': fuente,
        'region': region,
        'distrito': distrito_final(distrito_raw, PROPIOS) if distrito_raw else region,
        'institucion': entidad_final(raw.get('entidad', ''), PROPIOS),
        'cargo': cargo,
        'carreras': reglas.carreras_de(cargo, raw.get('cargo', '')),
        'sueldo': sueldo,
        'cierre': cierre,
        'numero': numero,
        'vacantes': vacantes,
        'tipo': 'Prácticas' if es_practica else tipo_desde_numero(numero),
        'modalidad': (raw.get('modalidad') or '').strip(),
        'indeterminado': '- INDETERMINADO' in numero,
        'ubicacion_raw': raw.get('ubicacion', ''),
        'clave_base': clave_base(region, raw.get('entidad', ''), raw.get('cargo', ''), numero, raw.get('ubicacion', '')),
        'cargo_raw': raw.get('cargo', ''),
    }


def motivo_descarte(rec, cfg, hoy):
    """Por qué NO se avisa esta oferta (None si sirve). `cfg` = sección «filtros» de config.json; `hoy` = date de Perú."""
    f = cfg['filtros']
    cargo_limpio = re.sub(r'[^A-Za-zÁÉÍÓÚÑáéíóúñ]', '', rec['cargo'])
    if len(cargo_limpio) < 6:
        return 'cargo basura'
    if MANUAL.search(rec['cargo_raw']):
        return 'labor manual'
    if OMITIR_CARGO.search(rec['cargo_raw']):
        return 'cargo cortado o con error'
    if rec['fuente'] != 'servir-practicas':
        if rec['tipo'] is None:
            return 'régimen no CAS ni 728'
        if not (f['sueldo_minimo'] <= (rec['sueldo'] or 0) <= f['sueldo_maximo']):
            return 'sueldo fuera de rango'
    if not rec['cierre']:
        return 'sin fecha de cierre'
    if date.fromisoformat(rec['cierre']) < hoy + timedelta(days=f['dias_minimos_abierta']):
        return 'cierra muy pronto o ya cerró'
    return reglas.evaluar(rec, cfg)  # tus reglas de región, cargo y carrera


def elegir(candidatas, cfg):
    """De las candidatas de UNA región: INDETERMINADO primero, luego la que cierra más tarde; máx. 1 por entidad en la primera pasada y
    `max_por_entidad` en la segunda; hasta `max_por_region`. Devuelve (elegidas, sobrantes)."""
    f = cfg['filtros']
    maximo = reglas.tope_region(candidatas[0]['region'], cfg) if candidatas else f['max_por_region']
    orden = sorted(candidatas, key=lambda r: r['cierre'], reverse=True)
    orden.sort(key=lambda r: not r['indeterminado'])
    elegidas, por_entidad = [], {}
    for tope in (1, f['max_por_entidad']):
        for r in orden:
            if len(elegidas) >= maximo:
                break
            if r in elegidas:
                continue
            if por_entidad.get(r['institucion'], 0) < tope:
                elegidas.append(r)
                por_entidad[r['institucion']] = por_entidad.get(r['institucion'], 0) + 1
    elegidas.sort(key=lambda r: r['cierre'], reverse=True)
    return elegidas, [r for r in orden if r not in elegidas]


def sin_repetidas(recs):
    """Quita las que quedan idénticas tras resumir (misma entidad, cargo, distrito y cierre)."""
    vistos, salida = set(), []
    for r in sorted(recs, key=lambda r: r['clave_base']):  # orden fijo: mañana se queda la misma
        k = (r['institucion'], r['cargo'], r['distrito'], r['cierre'], r['fuente'])
        if k in vistos:
            continue
        vistos.add(k)
        salida.append(r)
    return salida


def fecha_larga(iso):
    a, m, d = iso.split('-')
    return f'{d}/{m}/{a}'


def sueldo_texto(n):
    return f'S/. {n:,.2f}'


def documento(rec, id_):
    """Documento con los campos de `ConvocatoriaEstado` de UniNexo (listo para publicar)."""
    es_practica = rec['fuente'] == 'servir-practicas'
    vac = rec['vacantes']
    vacantes = f'{vac} {"vacante" if vac == 1 else "vacantes"}'
    donde = f'En SERVIR elige «Prácticas», Ubicación {nombre_servir(rec["region"])}' if es_practica else f'En SERVIR elige Ubicación {nombre_servir(rec["region"])}'
    clase = f' ({rec["modalidad"]})' if es_practica and rec['modalidad'] else ''
    doc = {
        'id': id_,
        'titulo': rec['cargo'],
        'cargo': rec['cargo'],
        'institucion': rec['institucion'],
        'departamento': rec['region'],
        'distrito': rec['distrito'],
        'tipo': rec['tipo'],
        'fechaCierre': rec['cierre'],
        'descripcion': f'{vacantes}. Publicada en el portal de SERVIR{clase} hasta el {fecha_larga(rec["cierre"])}; revisa en las bases el cronograma de inscripción. '
                       f'{donde} y busca la de {rec["institucion"]}, número de convocatoria: {rec["numero"]}.',
        'requisitos': 'El perfil y los requisitos están en las bases de la convocatoria (archivo Word) en el portal de SERVIR.',
        'enlaceOficial': URL_SERVIR_PRACTICAS if es_practica else URL_SERVIR_OFERTAS,
        'fuente': FUENTE_TEXTO,
        'estado': 'disponible',
        'destacada': False,
    }
    if rec.get('carreras'):
        doc['carrera'] = reglas.etiqueta_carreras(rec['carreras']).replace(', ', ' / ')
    if rec['sueldo']:
        doc['sueldo'] = sueldo_texto(rec['sueldo'])
        doc['sueldoNumero'] = rec['sueldo']
    return doc


def ids_para(recs, hoy):
    """ids únicos y estables para un lote: ce-<región>-<AAAAMMDD>-<nn>"""
    contador, salida = {}, []
    for r in recs:
        s = slug(r['region'])
        contador[s] = contador.get(s, 0) + 1
        salida.append(f'ce-{s}-{hoy.strftime("%Y%m%d")}-{contador[s]:02d}')
    return salida
