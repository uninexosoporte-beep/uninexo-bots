"""Normaliza el texto del portal SERVIR (todo en mayúsculas, sin tildes, con abreviaturas) para que se lea bien en UniNexo.

Sale del generador con el que se cargaron las 22 regiones de `convocatoriasRegiones.ts` (07/10/2026): mismas reglas y mismas
correcciones. Las listas ENTIDADES, DISTRITOS y CARGOS se pueden ir ampliando cuando aparezca un nombre mal escrito.
"""
import re
import unicodedata

DEPARTAMENTOS = ['Amazonas', 'Áncash', 'Apurímac', 'Arequipa', 'Ayacucho', 'Cajamarca', 'Callao', 'Cusco', 'Huancavelica', 'Huánuco', 'Ica', 'Junín',
                 'La Libertad', 'Lambayeque', 'Lima', 'Loreto', 'Madre de Dios', 'Moquegua', 'Pasco', 'Piura', 'Puno', 'San Martín', 'Tacna', 'Tumbes', 'Ucayali']

# Plazas de labor manual: no sirven para un universitario y no se avisan
MANUAL = re.compile(r'limpieza|recolecc|residuo|barrid|barrend|obrero|pe[oó]n\b|vigilan|vilante|serenazgo|sereno\b|chofer|conductor|ayudante|guardi[aá]n|jardin|cociner|portero|operario|'
                    r'mantenimiento|alba[nñ]il|lavander|costurer|mensajer|motorizado|centinela|custodi|ronder|cuadrill|trabajador de servicio|auxiliar de servicio|servicios? generales? \(?auxiliar|'
                    r'agente de seguridad|personal de seguridad|bombero|reci[eé]n nacid', re.I)
PEQUENAS = {'de', 'del', 'la', 'las', 'los', 'el', 'y', 'e', 'en', 'para', 'a', 'al', 'con', 'por', 'o', 'u', 'su', 'sus', 'un', 'una'}
# Siglas que se dejan en mayúsculas (entidades y cargos)
SIGLAS = set('''UGEL INPE ONP DIRESA GERESA DRE GRA MINEDU MIDIS MINSA MINAGRI MIDAGRI PNP SUNAT SUNARP RENIEC INEI SERFOR SERNANP OSINERGMIN PRONABEC PCM MTC MVCS MIMP MINJUSDH
PRODUCE SENASA INIA EPS ESSALUD SIS INABIF PNSR PRONACEJ ATU OSCE SUNEDU SENAMHI IIAP INDECI CENARES PRONAA CUNA PAE UNSA UNSAAC UNAMAD UNI UNMSM UNT UNP UNSCH UNH UNCP SERVIR MEF MINAM MINCETUR MINCUL
MIDIS MTPE MRE MINDEF MININTER MINJUS MINEM PRODUCE OEFA SUNASS OSIPTEL INDECOPI SBS SMV BCRP BN BNP PROINVERSION FONCODES PRONIED PRONATEL PROVIAS DGER OGA OCI TIC CAS RR SIAF SEACE SNIP INVIERTE
PNCVFS PNCM CEM UE HNAAA CAP DNI PPR PIP SSOMA GORE DEVIDA SIERRA JUNTOS CONADIS SUTRAN APN PROMPERU SENCICO SIS FISSAL IGP INGEMMET SEDAPAL SEDAPAR EMAPA CMAC AGRORURAL PSI PNIA EEAA UGE SAEI SIAGIE SIG SRE COAR OSCE SUNAFIL CEM RENUPSEP IAFAS SUCAMEC SANIPES IIEE PVL SISFOH'''.split())
ROMANOS = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX'}
# Plazas cuyo cargo viene cortado o con errores del portal y no se puede reescribir sin adivinar: se omiten
OMITIR_CARGO = re.compile(r'especilista|medicina intensa\b|^(centro de salud|puesto de salud|hospital)\b', re.I)
# Entidades que el portal abrevia o escribe cortadas: [texto en mayúsculas del portal] → nombre correcto
ENTIDADES = {
    'DEFENSORIA DEL PUEBLO': 'Defensoría del Pueblo',
    'UNIDAD EJECUTORA 404 SALUD LA CALETA': 'Unidad Ejecutora 404 Salud La Caleta',
    'MUNICIPALIDAD DISTRITAL DE PACHIA': 'Municipalidad Distrital de Pachía',
    'IAFAS DE LA MARINA DE GUERRA DEL PERU': 'IAFAS de la Marina de Guerra del Perú',
    'INSTITUTO DE INVESTIGACIONES DE LA AMAZONIA PERUANA': 'Instituto de Investigaciones de la Amazonía Peruana (IIAP)',
    'MUNICIPALIDAD DE LA PERLA': 'Municipalidad de La Perla',
    'MINISTERIO PUBLICO-GERENCIA GENERAL': 'Ministerio Público - Gerencia General',
    'ORGANISMO NACIONAL DE SANIDAD PESQUERA (SANIPES)': 'Organismo Nacional de Sanidad Pesquera (SANIPES)',
    'PROGR NAC PARA LA PREVENC Y ERRADIC DE LA VIOLENCIA CONTRA LAS MUJERES E INTEG DEL GRUP FAM-AURORA':
        'Programa Nacional para la Prevención y Erradicación de la Violencia contra las Mujeres e Integrantes del Grupo Familiar (AURORA)',
    'PROGRAMA NACIONAL CUNA MAS': 'Programa Nacional Cuna Más',
    'PROGRAMA NACIONAL DE ENTREGA DE LA PENSIÓN NO CONTRIBUTIVA A PERSONAS CON DISCAPACIDAD SEVERA EN SIT':
        'Programa Nacional de Entrega de la Pensión No Contributiva a Personas con Discapacidad Severa',
    'RED DE SALUD PACIFICO SUR': 'Red de Salud Pacífico Sur',
    'SUB REGION BAJO MAYO - TARAPOTO': 'Sub Región Bajo Mayo - Tarapoto',
    'SUPERINTENDENCIA NAC.SERV.DE SANEAMIENTO': 'Superintendencia Nacional de Servicios de Saneamiento (SUNASS)',
    'SUPERINTENDENCIA NACIONAL DE CONTROL DE SERVICIOS DE SEGURIDAD, ARMAS, MUNICIONES Y EXPLOSIVOS DE US':
        'Superintendencia Nacional de Control de Servicios de Seguridad, Armas, Municiones y Explosivos de Uso Civil (SUCAMEC)',
    'UND. DE GESTION EDUCATIVA LOCAL SAN MART': 'Unidad de Gestión Educativa Local San Martín',
    'UNIDAD DE GESTION EDUCATIVA LOCAL 01- EL PORVENIR': 'Unidad de Gestión Educativa Local 01 - El Porvenir',
    'UNIDAD DE GESTION EDUCATIVA LOCAL CELENDIN': 'Unidad de Gestión Educativa Local Celendín',
    'UNIDAD DE GESTION EDUCATIVA LOCAL DE MARAÑON': 'Unidad de Gestión Educativa Local de Marañón',
    'UNIDAD DE GESTION EDUCATIVA LOCAL- SULLANA': 'Unidad de Gestión Educativa Local - Sullana',
    'UNIDAD DE GESTION EDUCATIVA LOCAL- UGEL HUARMACA': 'Unidad de Gestión Educativa Local - UGEL Huarmaca',
    'UNIDAD EJECUTORA 303 SANCHEZ CERRO': 'Unidad Ejecutora 303 Sánchez Cerro',
    'UNIDAD EJECUTORIA 406 SALUD SANCHEZ CARRION': 'Unidad Ejecutora 406 Salud Sánchez Carrión',
    'UNIVERSIDAD NACIONAL AUTÓNOMA DE TAYACAJA DANIEL HERNANDEZ MORILLO': 'Universidad Nacional Autónoma de Tayacaja Daniel Hernández Morillo',
    'UNIVERSIDAD NACIONAL DE SAN CRISTOBAL DH': 'Universidad Nacional de San Cristóbal de Huamanga',
    'ZONA REGISTRAL # XII, SEDE AREQUIPA': 'Zona Registral N° XII - Sede Arequipa',
    'ZONA REGISTRAL I- SEDE PIURA': 'Zona Registral N° I - Sede Piura',
    'ZONA REGISTRAL NRO XI SEDE ICA': 'Zona Registral N° XI - Sede Ica',
    'ZONA REGISTRAL NRO. VIII - SEDE HUANCAYO': 'Zona Registral N° VIII - Sede Huancayo',
    'ZONA REGISTRAL N° XIV-SEDE AYACUCHO': 'Zona Registral N° XIV - Sede Ayacucho',
    'ZONA REGISTRAL NØ III SEDE MOYOBAMBA': 'Zona Registral N° III - Sede Moyobamba',
    'EMPRESA MUNICIPAL DE AGUA POTABLE Y ALCANTARILLADO DE BAGUA S.A.': 'Empresa Municipal de Agua Potable y Alcantarillado de Bagua S.A.',
    'INPE OFICINA REGIONAL ALTIPLANO PUNO': 'Instituto Nacional Penitenciario (INPE) - Oficina Regional Altiplano Puno',
    'GOBIERNO REGIONAL DE AREQUIPA -UGE NORTE': 'Gobierno Regional de Arequipa - UGE Norte',
}
# Distritos con tilde (el portal los escribe sin ella)
DISTRITOS = {'PAIJAN': 'Paiján', 'CHAMBARA': 'Chambará', 'CELENDIN': 'Celendín', 'CALLERIA': 'Callería', 'SAN JOSE DE QUERO': 'San José de Quero', 'CARAVELI': 'Caravelí',
             'SAN ANDRES': 'San Andrés', 'YURUA': 'Yurúa', 'PACHIA': 'Pachía', 'PUERTO BERMUDEZ': 'Puerto Bermúdez', 'JESUS NAZARENO': 'Jesús Nazareno',
             'JESUS MARIA': 'Jesús María', 'RIMAC': 'Rímac', 'BRENA': 'Breña', 'LURIN': 'Lurín', 'ANCON': 'Ancón', 'SAN MARTIN DE PORRES': 'San Martín de Porres',
             'HUANUCO': 'Huánuco', 'JUNIN': 'Junín', 'ANCASH': 'Áncash', 'APURIMAC': 'Apurímac', 'SAN MARTIN': 'San Martín',
             'CAMANA': 'Camaná', 'PACHACAMAC': 'Pachacámac', 'VILLA MARIA DEL TRIUNFO': 'Villa María del Triunfo', 'SANTA MARIA DEL MAR': 'Santa María del Mar',
             'ASCENSION': 'Ascensión', 'PERENE': 'Perené', 'RIO NEGRO': 'Río Negro', 'RIO TAMBO': 'Río Tambo', 'SAN RAMON': 'San Ramón', 'JESUS': 'Jesús',
             'JAEN': 'Jaén', 'JUANJUI': 'Juanjuí', 'SAN LUIS': 'San Luis', 'LA UNION': 'La Unión', 'HUARAZ': 'Huaraz', 'SANTA ROSA': 'Santa Rosa',
             'SAN SEBASTIAN': 'San Sebastián', 'SANTIAGO': 'Santiago', 'WANCHAQ': 'Wanchaq', 'YARINACOCHA': 'Yarinacocha', 'CORONEL PORTILLO': 'Coronel Portillo'}
# Cargos que el portal escribe con nombres propios o siglas que no se pueden deducir
CARGOS = {
    'AUXILIAR REGISTRAL PARA LA OFICINA REGISTRAL DE HUANCAYO': 'Auxiliar registral para la oficina registral de Huancayo',
    'MEDICO CENTRO DE SALUD SAN ANTONIO': 'Médico del Centro de Salud San Antonio',
    'TECNICO EN ENFERMERIA PARA CENTRO DE SALUD CARUMAS': 'Técnico en enfermería del Centro de Salud Carumas',
    'ESPECIALISTA EN GESTIÓN DE RIESGOS DE DESASTRES - UGEL SANTIAGO DE CHUCO Y UGEL JULCÁN': 'Especialista en gestión de riesgos de desastres (UGEL Santiago de Chuco y UGEL Julcán)',
    'COORDINADOR/A TÉCNICO EEAA VIRU': 'Coordinador/a técnico EEAA Virú',
    'RESPONSABLE DE PVL Y SISFOH': 'Responsable de PVL y SISFOH',
    'PROFESIONAL NO DOCENTE PARA EL SOPORTE Y ASESORAMIENTO A IIEE INCLUSIVAS': 'Profesional no docente para el soporte y asesoramiento a IIEE inclusivas',
    'PSICOLOGO(A)': 'Psicólogo(a)',
    'ARTICULADOR REGIONAL DEL REGISTRO NACIONAL DE UNIDADES PRESTADORAS DE SERVICIO DE EMPLEO (RENUPSEP)':
        'Articulador regional del registro nacional de unidades prestadoras de servicio de empleo (RENUPSEP)',
}
# Reescrituras de cargos largos del portal (sobre el texto en mayúsculas ya sin códigos)
COAR_RE = re.compile(r'^(.*?)\s+PARA EL COLEGIO DE ALTO (?:DE )?RENDIMIENTO DE (?:LA )?REGI.N (.+?)\s*-\s*(PLAZO DETERMINADO|SUPLENCIA TEMPORAL)\s*$')
CEM_RE = re.compile(r'^(.*?)\s+PARA EL CENTRO (?:DE )?EMERGENCIA MUJER\b.*$')
SAR_RE = re.compile(r'^(.*?)\s+PARA EL SERVICIO DE ATENCI.N RURAL \(SAR\).*$')
# Palabras que el portal escribe a menudo sin tilde
TILDES = {'educacion': 'educación', 'gestion': 'gestión', 'administracion': 'administración', 'contratacion': 'contratación', 'contrataciones': 'contrataciones',
          'informacion': 'información', 'comunicacion': 'comunicación', 'comunicaciones': 'comunicaciones', 'tecnologia': 'tecnología', 'tecnologias': 'tecnologías',
          'logistica': 'logística', 'logistico': 'logístico', 'tesoreria': 'tesorería', 'ingenieria': 'ingeniería', 'enfermeria': 'enfermería', 'psicologia': 'psicología',
          'economia': 'economía', 'auditoria': 'auditoría', 'prevencion': 'prevención', 'supervision': 'supervisión', 'coordinacion': 'coordinación', 'direccion': 'dirección',
          'evaluacion': 'evaluación', 'planificacion': 'planificación', 'formulacion': 'formulación', 'ejecucion': 'ejecución', 'operacion': 'operación', 'operaciones': 'operaciones',
          'produccion': 'producción', 'tecnico': 'técnico', 'tecnica': 'técnica', 'tecnicos': 'técnicos', 'medico': 'médico', 'medica': 'médica', 'asesoria': 'asesoría',
          'juridica': 'jurídica', 'juridico': 'jurídico', 'publica': 'pública', 'publico': 'público', 'publicas': 'públicas', 'publicos': 'públicos', 'area': 'área', 'areas': 'áreas',
          'tramite': 'trámite', 'inversion': 'inversión', 'inversiones': 'inversiones', 'informatica': 'informática', 'estadistica': 'estadística', 'biologo': 'biólogo',
          'quimico': 'químico', 'capacitacion': 'capacitación', 'actualizacion': 'actualización', 'organizacion': 'organización', 'atencion': 'atención',
          'pedagogica': 'pedagógica', 'pedagogico': 'pedagógico', 'academica': 'académica', 'academico': 'académico', 'matematica': 'matemática', 'fisica': 'física',
          'estrategica': 'estratégica', 'estrategico': 'estratégico', 'basica': 'básica', 'basico': 'básico', 'pagina': 'página', 'cartografia': 'cartografía',
          'topografia': 'topografía', 'geografia': 'geografía', 'electrica': 'eléctrica', 'electronica': 'electrónica', 'mecanica': 'mecánica', 'fiscalizacion': 'fiscalización',
          'sancion': 'sanción', 'conciliacion': 'conciliación', 'mediacion': 'mediación', 'afiliacion': 'afiliación', 'liquidacion': 'liquidación',
          'valorizacion': 'valorización', 'elaboracion': 'elaboración', 'implementacion': 'implementación', 'investigacion': 'investigación', 'promocion': 'promoción',
          'proteccion': 'protección', 'recaudacion': 'recaudación', 'nutricion': 'nutrición', 'odontologia': 'odontología', 'rehabilitacion': 'rehabilitación',
          'ninos': 'niños', 'nino': 'niño', 'ninas': 'niñas', 'nina': 'niña', 'ensenanza': 'enseñanza', 'diseno': 'diseño', 'pequenas': 'pequeñas', 'anos': 'años',
          'vehiculos': 'vehículos', 'vehiculo': 'vehículo', 'republica': 'república', 'numero': 'número', 'sociologia': 'sociología', 'antropologia': 'antropología',
          'consultoria': 'consultoría', 'agronomia': 'agronomía', 'pedagogia': 'pedagogía', 'digitalizacion': 'digitalización', 'documentacion': 'documentación',
          'inscripcion': 'inscripción', 'certificacion': 'certificación', 'identificacion': 'identificación', 'migracion': 'migración', 'poblacion': 'población',
          'regulacion': 'regulación', 'inspeccion': 'inspección', 'odontologo': 'odontólogo', 'tecnologo': 'tecnólogo', 'psicologo': 'psicólogo',
          'farmaceutico': 'farmacéutico', 'electrico': 'eléctrico', 'oftalmologo': 'oftalmólogo', 'analisis': 'análisis', 'diagnostico': 'diagnóstico',
          'economico': 'económico', 'politica': 'política', 'politico': 'político', 'practica': 'práctica', 'practicas': 'prácticas', 'pasantia': 'pasantía',
          'energia': 'energía', 'escalafon': 'escalafón', 'racionalizacion': 'racionalización', 'arqueologia': 'arqueología', 'geologia': 'geología',
          'teledeteccion': 'teledetección', 'seguiminento': 'seguimiento', 'maquinas': 'máquinas', 'telefonico': 'telefónico', 'orientacion': 'orientación',
          'indigena': 'indígena', 'traduccion': 'traducción', 'ultima': 'última', 'camara': 'cámara', 'camaras': 'cámaras', 'cartografico': 'cartográfico',
          'fotografo': 'fotógrafo', 'cientifico': 'científico', 'geografo': 'geógrafo', 'epidemiologia': 'epidemiología', 'epidemiologico': 'epidemiológico',
          'neonatologia': 'neonatología', 'oftalmologia': 'oftalmología', 'cardiologia': 'cardiología', 'pediatria': 'pediatría', 'ginecologia': 'ginecología',
          'radiologia': 'radiología', 'traumatologia': 'traumatología', 'anestesiologia': 'anestesiología', 'tecnologico': 'tecnológico', 'quimica': 'química',
          'martires': 'mártires', 'bibliotecologo': 'bibliotecólogo', 'civica': 'cívica', 'sesion': 'sesión', 'geofisico': 'geofísico', 'geologico': 'geológico',
          'hidrografico': 'hidrográfico', 'estadistico': 'estadístico', 'fiscalia': 'fiscalía', 'secretaria': 'secretaria'}
# Nombres propios que el portal escribe en mayúsculas dentro de cargos y entidades (se restauran después de pasar a minúsculas)
PROPIOS_FRASES = [('la libertad', 'La Libertad'), ('madre de dios', 'Madre de Dios'), ('san martin', 'San Martín'), ('san martín', 'San Martín'),
                  ('colegio de alto rendimiento', 'Colegio de Alto Rendimiento'), ('centro emergencia mujer', 'Centro Emergencia Mujer'),
                  ('servicio de atención rural', 'Servicio de Atención Rural'), ('perú', 'Perú'), ('peru', 'Perú')]
ABREV = [(r'\bMUNICIP\.?(?=\s|$)', 'MUNICIPALIDAD'), (r'\bMUNIC\.(?=\s|$)', 'MUNICIPALIDAD'), (r'\bGOB\.\s*REG\.?', 'GOBIERNO REGIONAL'),
         (r'\bDIST\.(?=\s|$)', 'DISTRITAL'), (r'\bPROV\.(?=\s|$)', 'PROVINCIAL'), (r'\bHOSP\.(?=\s|$)', 'HOSPITAL'), (r'\bUNID\.(?=\s|$)', 'UNIDAD'),
         (r'\bGERENC\.(?=\s|$)', 'GERENCIA'), (r'\bREG\.(?=\s|$)', 'REGIONAL'), (r'\bMINIST\.?(?=\s|$)', 'MINISTERIO'), (r'\bPUB LICO\b', 'PUBLICO'),
         (r'\bNRO\.?\s*(?=[0-9IVX])', 'N° '), (r'\bN\.\s*(?=\d)', 'N° '), (r'\bDIRECC?\.(?=\s|$)', 'DIRECCION')]
# Errores de tipeo frecuentes del portal: [mal escrito → bien escrito]
ERRATAS = {'admisnitrativo': 'administrativo', 'admisnitrativa': 'administrativa', 'administrtivo': 'administrativo', 'asistenet': 'asistente'}


def sin_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def slug(nombre):
    return re.sub(r'[^a-z0-9]+', '-', sin_tildes(nombre).lower()).strip('-')


def clave_texto(s):
    """Texto comparable: minúsculas, sin tildes ni signos, espacios simples."""
    return re.sub(r'[^a-z0-9]+', ' ', sin_tildes(s or '').lower()).strip()


def propios_departamentos():
    """Nombres de departamentos en el formato de la app, para restaurarlos dentro de cargos y entidades."""
    propios = {sin_tildes(d).upper(): d for d in DEPARTAMENTOS}
    propios.update({'PERU': 'Perú', 'ESTADO': 'Estado'})
    return propios


def departamento_desde_ubicacion(ubicacion):
    """'MADRE DE DIOS - TAMBOPATA' → ('Madre de Dios', 'TAMBOPATA')"""
    partes = (ubicacion or '').split(' - ', 1)
    base = sin_tildes(partes[0]).upper().strip()
    for d in DEPARTAMENTOS:
        if sin_tildes(d).upper() == base:
            return d, (partes[1].strip() if len(partes) > 1 else '')
    return None, (partes[1].strip() if len(partes) > 1 else '')


def palabra(tok, primera, propios, sentencia):
    """Una palabra: sigla, romano, nombre propio o minúscula (con tilde si está en el diccionario)."""
    nucleo = tok.strip('()[]«»",.;:')
    if not nucleo:
        return tok
    pos = tok.index(nucleo)
    pre, post = tok[:pos], tok[pos + len(nucleo):]
    base = sin_tildes(nucleo).upper()
    bajo = nucleo.lower()
    if base in SIGLAS or (nucleo.upper() == nucleo and nucleo in ROMANOS and len(nucleo) <= 4 and not primera):
        out = base if base in SIGLAS else nucleo
    elif base in propios:
        out = propios[base]
    else:
        out = nucleo
        if nucleo == nucleo.upper() or nucleo == nucleo.lower():
            out = TILDES.get(sin_tildes(bajo), bajo)
            if out == bajo and bajo == sin_tildes(bajo):  # sin tilde en el portal: reglas por terminación
                if re.search(r'(cion|sion)$', bajo):
                    out = bajo[:-4] + 'ción' if bajo.endswith('cion') else bajo[:-4] + 'sión'
                elif re.search(r'.{4,}gia$', bajo):
                    out = bajo[:-3] + 'gía'
                elif re.search(r'logic[oa]s?$', bajo):
                    out = re.sub(r'logic', 'lógic', bajo)
        if bajo in PEQUENAS and not primera:
            out = bajo
        elif not sentencia and bajo not in PEQUENAS:
            out = out[:1].upper() + out[1:]
        elif primera:
            out = out[:1].upper() + out[1:]
    return pre + out + post


def caso(texto, propios, sentencia):
    """Convierte MAYÚSCULAS del portal: sentencia=True → «Especialista en contabilidad»; False → «Municipalidad Distrital de San Pablo»."""
    for pat, rep in ABREV:
        texto = re.sub(pat, rep, texto)
    for mal, bien in ERRATAS.items():
        texto = re.sub(r'\b' + mal + r'\b', bien.upper(), texto, flags=re.I)
    texto = re.sub(r'N\s*[°ºø#]\s*', 'N° ', texto)           # «Nø III», «# XII», «N°VI» → «N° III»
    texto = re.sub(r'\s*#\s*', ' N° ', texto)
    texto = re.sub(r'\s+', ' ', texto.strip())
    partes = re.split(r'(\s+|-|/)', texto)
    out, primera = [], True
    for p in partes:
        if not p or re.fullmatch(r'\s+|-|/', p):
            out.append(p)
            continue
        if re.fullmatch(r'(?:[A-Za-z]\.){2,}[A-Za-z]?\.?', p):  # S.R.E. → SRE
            out.append(p.replace('.', '').upper())
            primera = False
            continue
        out.append(palabra(p, primera, propios, sentencia))
        primera = False
    res = ''.join(out)
    for frase, bien in PROPIOS_FRASES:
        res = re.sub(r'\b' + re.escape(frase) + r'\b', bien, res, flags=re.I)
    res = re.sub(r'\s+-\s*', ' - ', res)                      # guion siempre con espacios
    res = re.sub(r'(?<=\w)-\s+', ' - ', res)                  # «I- auxiliar» → «I - auxiliar»
    if not sentencia:
        res = re.sub(r'( - |: )([a-záéíóúñ])', lambda m: m.group(1) + m.group(2).upper(), res)
    return res


def sueldo_num(txt):
    m = re.search(r'([\d,]+(?:\.\d+)?)', txt or '')
    return float(m.group(1).replace(',', '')) if m else 0.0


def limpiar_cargo(c):
    c = re.sub(r'\s*\(\s*\d{3,}\s*\)\s*', ' ', c).strip()
    c = c.replace('"', '').replace('“', '').replace('”', '')
    c = re.sub(r'^CONTRATACI.N ADMINISTRATIVA DE SERVICIOS DE (UN\(A\)|UN/A|UNA|UN)?\s*', '', c, flags=re.I)
    c = re.sub(r'^(CONTRATAR LOS SERVICIOS DE|SUPLENCIA DE)\s+', '', c, flags=re.I)
    c = re.sub(r'^(UN/A|UN\(A\)|UNA|UN|DOS|TRES)\s*\(\s*\d+\s*\)\s*', '', c, flags=re.I)  # «un/a (01) …», «Dos (02) …»
    c = re.sub(r'^\(\s*\d+\s*\)\s*', '', c)                                              # «(01) técnico …»
    c = re.sub(r'^(UN/A|UN\(A\)|UNA|UN)\s+(?=[A-ZÁÉÍÓÚÑ])', '', c)
    c = re.sub(r'^CONVOCATORIA PARA LA CONTRATACI.N ADMINISTRATIVA DE SERVICIO CAS \(NECESIDAD TRANSITORIA\)\s*', '', c, flags=re.I)
    c = re.sub(r'^(UN/A|UN\(A\)|UNA|UN)\s*\(\s*\d+\s*\)\s*', '', c, flags=re.I)
    c = re.sub(r'\s*\(CONTRATO A PLAZO DETERMINADO[^)]*\)', '', c, flags=re.I)
    c = c.rstrip('. ')
    return c.strip()


def cargo_final(raw, propios):
    """Cargo legible: los largos de los colegios de alto rendimiento y de los Centros Emergencia Mujer se resumen sin perder el cargo."""
    if raw in CARGOS:
        return CARGOS[raw]
    c = limpiar_cargo(raw)
    m = COAR_RE.match(c)
    if m:
        parte, region, tipo = m.groups()
        parte = re.sub(r'^DOCENTE PARA LA (ENSE.ANZA DE LA )?ASIGNATURA DE ', 'DOCENTE DE ', parte)
        reg = propios.get(sin_tildes(region.strip()).upper()) or caso(region, propios, False)
        extra = ', suplencia temporal' if tipo.startswith('SUPLENCIA') else ''
        return f'{caso(parte, propios, True)} (Colegio de Alto Rendimiento de la región {reg}{extra})'
    m = CEM_RE.match(c)
    if m:
        return f'{caso(m.group(1), propios, True)} del Centro Emergencia Mujer (CEM)'
    m = SAR_RE.match(c)
    if m:
        return f'{caso(m.group(1), propios, True)} del Servicio de Atención Rural (SAR)'
    return caso(c, propios, True)


def entidad_final(raw, propios):
    return ENTIDADES.get(raw) or caso(raw, propios, False)


def distrito_final(raw, propios):
    return DISTRITOS.get(raw) or caso(raw, propios, False)


def fecha_iso(fin):
    """'21/10/2026' → '2026-10-21'  (None si no tiene ese formato)"""
    m = re.fullmatch(r'\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*', fin or '')
    if not m:
        return None
    return f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
