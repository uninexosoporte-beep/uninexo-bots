import { createRequire } from 'module'; const require = createRequire(import.meta.url);

// scripts/blog-entradas-bot.ts
import { writeFileSync } from "node:fs";

// src/data/peruUniversities.ts
var PERU_UNIVERSITIES = [
  // =============================================================
  // 🏛️ UNIVERSIDADES PÚBLICAS Y PRIVADAS - AUDITORÍA SUNEDU (BLOQUE 1 DE 5 EN 5)
  // =============================================================
  // 1. UNMSM - Universidad Nacional Mayor de San Marcos
  {
    id: "unmsm",
    acronym: "UNMSM",
    name: "Universidad Nacional Mayor de San Marcos",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#003366",
    type: "publica",
    sedes: [
      { id: "unmsm-ciudad-universitaria", name: "Ciudad Universitaria (Av. Venezuela / Av. Universitaria, Cercado de Lima)", city: "Lima" },
      { id: "unmsm-san-fernando", name: "Facultad de Medicina San Fernando (Av. Miguel Grau 755, Cercado de Lima)", city: "Lima" },
      { id: "unmsm-sjl", name: "Sede San Juan de Lurigancho (Av. Fernando Wiesse)", city: "Lima" },
      { id: "unmsm-huaral", name: "Sede Huaral", city: "Lima Provincias" },
      { id: "unmsm-chilca", name: "Sede Chilca", city: "Lima Provincias" },
      { id: "unmsm-oyon", name: "Sede Oy\xF3n", city: "Lima Provincias" },
      { id: "unmsm-chancay", name: "Sede Chancay", city: "Lima Provincias" },
      { id: "unmsm-huarmey", name: "Sede Huarmey", city: "\xC1ncash" },
      { id: "unmsm-villa-rica", name: "Sede Villa Rica", city: "Pasco" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Administraci\xF3n de Negocios Internacionales",
      "Administraci\xF3n de Turismo",
      "Antropolog\xEDa",
      "Arqueolog\xEDa",
      "Arquitectura y Urbanismo",
      "Arte",
      "Bibliotecolog\xEDa y Ciencias de la Informaci\xF3n",
      "Biolog\xEDa con menci\xF3n en Hidrobiolog\xEDa y Pesquer\xEDa",
      "Biolog\xEDa con menci\xF3n en Zoolog\xEDa",
      "Ciencia Pol\xEDtica",
      "Ciencias de la Computaci\xF3n",
      "Comunicaci\xF3n Social",
      "Conservaci\xF3n y Restauraci\xF3n",
      "Contabilidad",
      "Danza",
      "Derecho",
      "Econom\xEDa",
      "Econom\xEDa Internacional",
      "Econom\xEDa P\xFAblica",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Estad\xEDstica",
      "Farmacia y Bioqu\xEDmica",
      "Filosof\xEDa",
      "F\xEDsica",
      "Gen\xE9tica y Biotecnolog\xEDa",
      "Geograf\xEDa",
      "Gesti\xF3n Tributaria",
      "Historia",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Biom\xE9dica",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Seguridad y Salud en el Trabajo",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa de Software",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Geogr\xE1fica",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica de Fluidos",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Qu\xEDmica",
      "Ingenier\xEDa Textil y Confecciones",
      "Investigaci\xF3n Operativa",
      "Ling\xFC\xEDstica",
      "Literatura",
      "Matem\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Microbiolog\xEDa y Parasitolog\xEDa",
      "Nutrici\xF3n",
      "Obstetricia",
      "Odontolog\xEDa",
      "Psicolog\xEDa",
      "Psicolog\xEDa Organizacional y de la Gesti\xF3n Humana",
      "Qu\xEDmica",
      "Sociolog\xEDa",
      "Tecnolog\xEDa M\xE9dica en Laboratorio Cl\xEDnico y Anatom\xEDa Patol\xF3gica",
      "Tecnolog\xEDa M\xE9dica en Radiolog\xEDa",
      "Tecnolog\xEDa M\xE9dica en Terapia F\xEDsica y Rehabilitaci\xF3n",
      "Tecnolog\xEDa M\xE9dica en Terapia Ocupacional",
      "Trabajo Social"
    ]
  },
  // 2. UNI - Universidad Nacional de Ingeniería
  {
    id: "uni",
    acronym: "UNI",
    name: "Universidad Nacional de Ingenier\xEDa",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#800000",
    type: "publica",
    sedes: [
      { id: "uni-campus-central", name: "Campus Central (Av. T\xFApac Amaru 210, R\xEDmac)", city: "Lima" }
    ],
    carreras: [
      "Arquitectura",
      "Ciencia de la Computaci\xF3n",
      "F\xEDsica",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Petr\xF3leo y Gas Natural",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa de Telecomunicaciones",
      "Ingenier\xEDa El\xE9ctrica",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Estad\xEDstica",
      "Ingenier\xEDa F\xEDsica",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Higiene y Seguridad Industrial",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Mec\xE1nica El\xE9ctrica",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Naval",
      "Ingenier\xEDa Petroqu\xEDmica",
      "Ingenier\xEDa Qu\xEDmica",
      "Ingenier\xEDa Sanitaria",
      "Ingenier\xEDa Textil",
      "Matem\xE1tica",
      "Qu\xEDmica",
      "Urbanismo"
    ]
  },
  // 3. UNALM - Universidad Nacional Agraria La Molina
  {
    id: "unalm",
    acronym: "UNALM",
    name: "Universidad Nacional Agraria La Molina",
    logo: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=120&auto=format&fit=crop&q=80",
    color: "#1B4D3E",
    type: "publica",
    sedes: [
      { id: "unalm-la-molina-central", name: "Campus La Molina (Av. La Molina s/n, La Molina)", city: "Lima" }
    ],
    carreras: [
      "Agronom\xEDa",
      "Biolog\xEDa",
      "Econom\xEDa",
      "Estad\xEDstica Inform\xE1tica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa de Gesti\xF3n Empresarial",
      "Ingenier\xEDa en Industrias Alimentarias",
      "Ingenier\xEDa Forestal",
      "Meteorolog\xEDa",
      "Pesquer\xEDa",
      "Zootecnia"
    ]
  },
  // 4. UNFV - Universidad Nacional Federico Villarreal
  {
    id: "unfv",
    acronym: "UNFV",
    name: "Universidad Nacional Federico Villarreal",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "publica",
    sedes: [
      { id: "unfv-rectorado", name: "Sede Central - Rectorado (Cercado de Lima)", city: "Lima" },
      { id: "unfv-el-agustino", name: "Sede El Agustino - Facultad de Medicina / Salud", city: "Lima" },
      { id: "unfv-miraflores", name: "Sede Miraflores - Facultad de Educaci\xF3n", city: "Lima" },
      { id: "unfv-jesus-maria", name: "Sede Jes\xFAs Mar\xEDa - Odontolog\xEDa", city: "Lima" },
      { id: "unfv-san-miguel", name: "Sede San Miguel - Ciencias Econ\xF3micas y Financieras", city: "Lima" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Administraci\xF3n del Turismo",
      "Administraci\xF3n P\xFAblica",
      "Antropolog\xEDa",
      "Arqueolog\xEDa",
      "Arquitectura",
      "Biolog\xEDa",
      "Ciencia Pol\xEDtica",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico-Sociales",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Lenguas Extranjeras",
      "Educaci\xF3n Secundaria en Matem\xE1tica y F\xEDsica",
      "Enfermer\xEDa",
      "Estad\xEDstica",
      "Farmacia y Bioqu\xEDmica",
      "Filosof\xEDa",
      "F\xEDsica",
      "Geograf\xEDa",
      "Historia",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa de Transportes",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Geogr\xE1fica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Inform\xE1tica",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Ling\xFC\xEDstica",
      "Literatura",
      "Matem\xE1tica",
      "Medicina Humana",
      "Nutrici\xF3n",
      "Obstetricia",
      "Odontolog\xEDa",
      "Psicolog\xEDa",
      "Qu\xEDmica",
      "Sociolog\xEDa",
      "Tecnolog\xEDa M\xE9dica en Laboratorio Cl\xEDnico y Anatom\xEDa Patol\xF3gica",
      "Tecnolog\xEDa M\xE9dica en Radiolog\xEDa",
      "Tecnolog\xEDa M\xE9dica en Terapia F\xEDsica y Rehabilitaci\xF3n",
      "Tecnolog\xEDa M\xE9dica en Terapia del Lenguaje",
      "Trabajo Social"
    ]
  },
  // 5. UNE - Universidad Nacional de Educación Enrique Guzmán y Valle "La Cantuta"
  {
    id: "une",
    acronym: "UNE",
    name: 'Universidad Nacional de Educaci\xF3n Enrique Guzm\xE1n y Valle "La Cantuta"',
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "publica",
    sedes: [
      { id: "une-chosica-central", name: "Campus Central Chosica (Lurigancho-Chosica)", city: "Lima" },
      { id: "une-la-molina", name: "Sede La Molina (Av. Los Mirlos)", city: "Lima" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Administraci\xF3n de Negocios Internacionales",
      "Agropecuaria",
      "Artes Esc\xE9nicas",
      "Artes Pl\xE1sticas",
      "Biolog\xEDa y Ciencias Naturales",
      "Construcci\xF3n Civil",
      "Desarrollo Humano",
      "Dise\xF1os Tecnol\xF3gicos",
      "Ebanister\xEDa y Decoraci\xF3n",
      "Educaci\xF3n B\xE1sica Alternativa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Electricidad",
      "Electr\xF3nica e Inform\xE1tica",
      "Gastronom\xEDa",
      "Geograf\xEDa",
      "Historia",
      "Industrias Alimentarias",
      "Inform\xE1tica",
      "Ingl\xE9s",
      "Lengua Espa\xF1ola",
      "Literatura",
      "Matem\xE1tica e Inform\xE1tica",
      "Mec\xE1nica de Producci\xF3n",
      "Metalurgia y Joyer\xEDa",
      "M\xFAsica",
      "Nutrici\xF3n Humana",
      "Qu\xEDmica y Biolog\xEDa",
      "Textil y Confecciones",
      "Turismo y Hoteler\xEDa"
    ]
  },
  {
    id: "unac",
    acronym: "UNAC",
    name: "Universidad Nacional del Callao",
    logo: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "publica",
    sedes: [
      { id: "unac-bellavista", name: "Campus Principal (Av. Juan Pablo II 306, Bellavista)", city: "Callao" },
      { id: "unac-canete", name: "Filial Ca\xF1ete (Fundo El Arbolito, San Luis)", city: "Lima Provincias" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Contabilidad",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Enfermer\xEDa",
      "F\xEDsica",
      "Ingenier\xEDa Ambiental y de Recursos Naturales",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa El\xE9ctrica",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1tica"
    ]
  },
  {
    id: "untels",
    acronym: "UNTELS",
    name: "Universidad Nacional Tecnol\xF3gica de Lima Sur",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#2563EB",
    type: "publica",
    sedes: [
      { id: "untels-ves", name: "Campus Villa El Salvador (Av. Central con Av. Bol\xEDvar)", city: "Lima" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Electr\xF3nica y Telecomunicaciones",
      "Ingenier\xEDa Mec\xE1nica y El\xE9ctrica"
    ]
  },
  {
    id: "undc",
    acronym: "UNDC",
    name: "Universidad Nacional de Ca\xF1ete",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#059669",
    type: "publica",
    sedes: [
      { id: "undc-san-vicente", name: "Campus San Vicente de Ca\xF1ete (Av. Mariscal Benavides)", city: "Lima Provincias" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Administraci\xF3n de Turismo y Hoteler\xEDa",
      "Agronom\xEDa",
      "Contabilidad",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  {
    id: "unab",
    acronym: "UNAB",
    name: "Universidad Nacional de Barranca",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#D97706",
    type: "publica",
    sedes: [
      { id: "unab-barranca", name: "Campus Barranca (Av. Toribio de Luzuriaga Mz. J)", city: "Lima Provincias" }
    ],
    carreras: [
      "Contabilidad y Finanzas",
      "Derecho y Ciencias Pol\xEDticas",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa de Industrias Alimentarias",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Obstetricia"
    ]
  },
  {
    id: "unjfsc",
    acronym: "UNJFSC",
    name: "Universidad Nacional Jos\xE9 Faustino S\xE1nchez Carri\xF3n",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#7C2D12",
    type: "publica",
    sedes: [
      { id: "unjfsc-huacho", name: "Campus Universitario Huacho (Av. Mercedes Indacochea 600)", city: "Lima Provincias" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Biolog\xEDa con menci\xF3n en Biotecnolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa y Finanzas",
      "Educaci\xF3n F\xEDsica y Deportes",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria y Problemas de Aprendizaje",
      "Educaci\xF3n Secundaria en Biolog\xEDa, Qu\xEDmica y Tecnolog\xEDa de Alimentos",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico Sociales y Turismo",
      "Educaci\xF3n Secundaria en Ingl\xE9s",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Matem\xE1tica, F\xEDsica e Inform\xE1tica",
      "Enfermer\xEDa",
      "Estad\xEDstica e Inform\xE1tica",
      "F\xEDsica",
      "Ingenier\xEDa Agron\xF3mica",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Inform\xE1tica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1ticas Aplicadas",
      "Medicina Humana",
      "Negocios Internacionales",
      "Obstetricia",
      "Sociolog\xEDa",
      "Trabajo Social",
      "Turismo y Hoteler\xEDa",
      "Zootecnia"
    ]
  },
  {
    id: "unm",
    acronym: "UNM",
    name: "Universidad Nacional de M\xFAsica",
    logo: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=120&auto=format&fit=crop&q=80",
    color: "#9333EA",
    type: "publica",
    sedes: [
      { id: "unm-emancipacion", name: "Sede Principal (Av. Emancipaci\xF3n 180, Cercado de Lima)", city: "Lima" },
      { id: "unm-carabaya", name: "Sede Anexo (Jr. Carabaya 421, Cercado de Lima)", city: "Lima" }
    ],
    carreras: [
      "Composici\xF3n Musical",
      "Direcci\xF3n Coral",
      "Direcci\xF3n Orquestal",
      "Educaci\xF3n Musical",
      "Interpretaci\xF3n Musical en Arpa",
      "Interpretaci\xF3n Musical en Canto",
      "Interpretaci\xF3n Musical en Clarinete",
      "Interpretaci\xF3n Musical en Contrabajo",
      "Interpretaci\xF3n Musical en Corno",
      "Interpretaci\xF3n Musical en Fagot",
      "Interpretaci\xF3n Musical en Flauta Traversa",
      "Interpretaci\xF3n Musical en Guitarra",
      "Interpretaci\xF3n Musical en Oboe",
      "Interpretaci\xF3n Musical en Percusi\xF3n",
      "Interpretaci\xF3n Musical en Piano",
      "Interpretaci\xF3n Musical en Saxof\xF3n",
      "Interpretaci\xF3n Musical en Tromb\xF3n",
      "Interpretaci\xF3n Musical en Trompeta",
      "Interpretaci\xF3n Musical en Tuba",
      "Interpretaci\xF3n Musical en Viola",
      "Interpretaci\xF3n Musical en Viol\xEDn",
      "Interpretaci\xF3n Musical en Violonchelo",
      "Musicolog\xEDa"
    ]
  },
  // -------------------------------------------------------------
  // 🌊 2. Norte del Perú (15)
  // -------------------------------------------------------------
  {
    id: "unt",
    acronym: "UNT",
    name: "Universidad Nacional de Trujillo",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#0369A1",
    type: "publica",
    sedes: [
      { id: "unt-trujillo", name: "Ciudad Universitaria (Av. Juan Pablo II s/n, Trujillo)", city: "La Libertad" },
      { id: "unt-valle-jequetepeque", name: "Filial Valle Jequetepeque (Guadalupe)", city: "La Libertad" },
      { id: "unt-huamachuco", name: "Filial Huamachuco (S\xE1nchez Carri\xF3n)", city: "La Libertad" },
      { id: "unt-santiago-de-chuco", name: "Filial Santiago de Chuco", city: "La Libertad" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Antropolog\xEDa",
      "Arqueolog\xEDa",
      "Arquitectura y Urbanismo",
      "Biolog\xEDa Pesquera",
      "Biotecnolog\xEDa",
      "Ciencia Pol\xEDtica y Gobernabilidad",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad y Finanzas",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Matem\xE1ticas",
      "Educaci\xF3n Secundaria en Ciencias Naturales",
      "Educaci\xF3n Secundaria en Filosof\xEDa, Psicolog\xEDa y Ciencias Sociales",
      "Educaci\xF3n Secundaria en Historia y Geograf\xEDa",
      "Educaci\xF3n Secundaria en Idiomas e Ingl\xE9s",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Enfermer\xEDa",
      "Estomatolog\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "F\xEDsica",
      "Historia",
      "Inform\xE1tica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Materiales",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1ticas",
      "Medicina Humana",
      "Microbiolog\xEDa y Parasitolog\xEDa",
      "Trabajo Social",
      "Turismo"
    ]
  },
  {
    id: "unca",
    acronym: "UNCA",
    name: "Universidad Nacional Ciro Alegr\xEDa",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "publica",
    sedes: [
      { id: "unca-huamachuco", name: "Campus Huamachuco (Jr. Balta 434, S\xE1nchez Carri\xF3n)", city: "La Libertad" }
    ],
    carreras: [
      "Gesti\xF3n Empresarial y Emprendimiento",
      "Ingenier\xEDa Agr\xEDcola y Forestal",
      "Ingenier\xEDa de Minas y Geolog\xEDa"
    ]
  },
  {
    id: "unp",
    acronym: "UNP",
    name: "Universidad Nacional de Piura",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "publica",
    sedes: [
      { id: "unp-piura", name: "Campus Universitario Miraflores (Castilla, Piura)", city: "Piura" },
      { id: "unp-sullana", name: "Filial Sullana", city: "Piura" },
      { id: "unp-chulucanas", name: "Filial Chulucanas", city: "Piura" },
      { id: "unp-huancabamba", name: "Filial Huancabamba", city: "Piura" },
      { id: "unp-paita", name: "Filial Paita", city: "Piura" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Agronom\xEDa",
      "Arquitectura y Urbanismo",
      "Biolog\xEDa",
      "Ciencias de la Comunicaci\xF3n Social",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico-Geogr\xE1ficas",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Matem\xE1tica y F\xEDsica",
      "Enfermer\xEDa",
      "Estad\xEDstica",
      "F\xEDsica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental y de Recursos Naturales",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Petr\xF3leo",
      "Ingenier\xEDa Electr\xF3nica y Telecomunicaciones",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Inform\xE1tica",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Obstetricia"
    ]
  },
  {
    id: "unf",
    acronym: "UNF",
    name: "Universidad Nacional de Frontera",
    logo: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "publica",
    sedes: [
      { id: "sullana-central", name: "Campus Universitario Sullana (Av. San Hilari\xF3n s/n)", city: "Piura" }
    ],
    carreras: [
      "Administraci\xF3n de Hoteler\xEDa y Turismo",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa de Industrias Alimentarias",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Forestal"
    ]
  },
  // 16. UNPRG - Universidad Nacional Pedro Ruiz Gallo
  {
    id: "unprg",
    acronym: "UNPRG",
    name: "Universidad Nacional Pedro Ruiz Gallo",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "publica",
    sedes: [
      { id: "unprg-lambayeque", name: "Campus Universitario Lambayeque (Av. Juan XXIII 391)", city: "Lambayeque" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Arquitectura",
      "Biolog\xEDa con menci\xF3n en Bot\xE1nica",
      "Biolog\xEDa con menci\xF3n en Microbiolog\xEDa y Parasitolog\xEDa",
      "Biolog\xEDa con menci\xF3n en Pesquer\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Computaci\xF3n e Inform\xE1tica",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico Sociales y Filosof\xEDa",
      "Educaci\xF3n Secundaria en Ciencias Naturales",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Lenguas Extranjeras",
      "Educaci\xF3n Secundaria en Matem\xE1tica y Computaci\xF3n",
      "Enfermer\xEDa",
      "Estad\xEDstica",
      "F\xEDsica",
      "Historia",
      "Industrias Alimentarias",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Computaci\xF3n e Inform\xE1tica",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica y El\xE9ctrica",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1ticas",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Sociolog\xEDa",
      "Zootecnia"
    ]
  },
  // 17. UNTUMBES - Universidad Nacional de Tumbes
  {
    id: "untumbes",
    acronym: "UNTUMBES",
    name: "Universidad Nacional de Tumbes",
    logo: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=120&auto=format&fit=crop&q=80",
    color: "#0D9488",
    type: "publica",
    sedes: [
      { id: "untumbes-central", name: "Campus Pampa de San Isidro (Av. Universitaria s/n)", city: "Tumbes" },
      { id: "untumbes-arica", name: "Sede Ciudad de Tumbes (Av. Arica 361)", city: "Tumbes" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agroindustria",
      "Agronom\xEDa",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Forestal y Medio Ambiente",
      "Ingenier\xEDa Industrial Pesquera",
      "Medicina Humana",
      "Medicina Veterinaria y Zootecnia",
      "Nutrici\xF3n y Diet\xE9tica",
      "Obstetricia",
      "Psicolog\xEDa",
      "Turismo"
    ]
  },
  // 18. UNS - Universidad Nacional del Santa
  {
    id: "uns",
    acronym: "UNS",
    name: "Universidad Nacional del Santa",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#2563EB",
    type: "publica",
    sedes: [
      { id: "uns-nuevo-chimbote", name: "Campus Universitario Nuevo Chimbote (Av. Universitaria s/n, Urb. Bellamar)", city: "\xC1ncash" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Biolog\xEDa en Acuicultura",
      "Biotecnolog\xEDa",
      "Comunicaci\xF3n Social",
      "Derecho y Ciencias Pol\xEDticas",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Naturales",
      "Educaci\xF3n Secundaria en Historia, Geograf\xEDa y Ciencias Sociales",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Matem\xE1tica, Computaci\xF3n e Inform\xE1tica",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa Mec\xE1nica",
      "Medicina Humana"
    ]
  },
  // 19. UNASAM - Universidad Nacional Santiago Antúnez de Mayolo
  {
    id: "unasam",
    acronym: "UNASAM",
    name: "Universidad Nacional Santiago Ant\xFAnez de Mayolo",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#C2410C",
    type: "publica",
    sedes: [
      { id: "unasam-huaraz", name: "Campus Shancay\xE1n (Av. Centenario 200, Huaraz)", city: "\xC1ncash" },
      { id: "unasam-tingua", name: "Campus Tingua (Monga, Yungay)", city: "\xC1ncash" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Arqueolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria e Intercultural Biling\xFCe",
      "Educaci\xF3n Secundaria en Ciencias Naturales",
      "Educaci\xF3n Secundaria en Lengua Castellana y Literatura",
      "Educaci\xF3n Secundaria en Lengua Extranjera: Ingl\xE9s",
      "Educaci\xF3n Secundaria en Matem\xE1tica e Inform\xE1tica",
      "Enfermer\xEDa",
      "Estad\xEDstica e Inform\xE1tica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Sanitaria",
      "Obstetricia",
      "Turismo"
    ]
  },
  // 20. UNC - Universidad Nacional de Cajamarca
  {
    id: "unc",
    acronym: "UNC",
    name: "Universidad Nacional de Cajamarca",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#1E40AF",
    type: "publica",
    sedes: [
      { id: "unc-cajamarca", name: "Campus Principal San Mart\xEDn (Av. Atahualpa 1050)", city: "Cajamarca" },
      { id: "unc-jaen", name: "Filial Ja\xE9n", city: "Cajamarca" },
      { id: "unc-chota", name: "Filial Chota", city: "Cajamarca" },
      { id: "unc-bambamarca", name: "Filial Bambamarca", city: "Cajamarca" },
      { id: "unc-celendin", name: "Filial Celend\xEDn", city: "Cajamarca" },
      { id: "unc-cajabamba", name: "Filial Cajabamba", city: "Cajamarca" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Biolog\xEDa y Biotecnolog\xEDa",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Naturales, Qu\xEDmica y Biolog\xEDa",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Lenguas Extranjeras",
      "Educaci\xF3n Secundaria en Matem\xE1tica y F\xEDsica",
      "Enfermer\xEDa",
      "Estad\xEDstica",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Forestal",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Hidr\xE1ulica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Zootecnista",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Obstetricia",
      "Sociolog\xEDa",
      "Turismo y Hoteler\xEDa"
    ]
  },
  // 21. UNACH - Universidad Nacional Autónoma de Chota
  {
    id: "unach",
    acronym: "UNACH",
    name: "Universidad Nacional Aut\xF3noma de Chota",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#059669",
    type: "publica",
    sedes: [
      { id: "unach-colpa-matara", name: "Campus Colpa Matara (Chota)", city: "Cajamarca" }
    ],
    carreras: [
      "Contabilidad",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Forestal y Ambiental"
    ]
  },
  // 22. UNJ - Universidad Nacional de Jaén
  {
    id: "unj",
    acronym: "UNJ",
    name: "Universidad Nacional de Ja\xE9n",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#D97706",
    type: "publica",
    sedes: [
      { id: "unj-yanuyacu", name: "Campus Yanuyacu (Sector Yanuyacu, Ja\xE9n)", city: "Cajamarca" }
    ],
    carreras: [
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Industrias Alimentarias",
      "Ingenier\xEDa de Tecnolog\xEDas de la Informaci\xF3n y Comunicaciones",
      "Ingenier\xEDa Forestal y Ambiental",
      "Ingenier\xEDa Mec\xE1nica y El\xE9ctrica"
    ]
  },
  // 23. UNTEFSIL - Universidad Nacional Tecnológica de Frontera San Ignacio de Loyola
  {
    id: "untefsil",
    acronym: "UNTEFSIL",
    name: "Universidad Nacional Tecnol\xF3gica de Frontera San Ignacio de Loyola",
    logo: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=120&auto=format&fit=crop&q=80",
    color: "#047857",
    type: "publica",
    sedes: [
      { id: "untefsil-san-ignacio", name: "Campus San Ignacio (Av. San Ignacio s/n)", city: "Cajamarca" }
    ],
    carreras: [
      "Administraci\xF3n Ecotur\xEDstica",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Forestal y Ambiental"
    ]
  },
  // 24. UNTRM - Universidad Nacional Toribio Rodríguez de Mendoza
  {
    id: "untrm",
    acronym: "UNTRM",
    name: "Universidad Nacional Toribio Rodr\xEDguez de Mendoza",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#7C2D12",
    type: "publica",
    sedes: [
      { id: "untrm-chachapoyas", name: "Campus Universitario Higos Urco (Chachapoyas)", city: "Amazonas" },
      { id: "untrm-utcubamba", name: "Filial Utcubamba (Bagua Grande)", city: "Amazonas" },
      { id: "untrm-rodriguez-mendoza", name: "Filial Rodr\xEDguez de Mendoza (Mendoza)", city: "Amazonas" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Administraci\xF3n de Turismo",
      "Agronom\xEDa",
      "Arqueolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Forestal",
      "Ingenier\xEDa Zootecnista",
      "Medicina Humana",
      "Psicolog\xEDa"
    ]
  },
  // 25. UNIFSLB - Universidad Nacional Intercultural Fabiola Salazar Leguía de Bagua
  {
    id: "unifslb",
    acronym: "UNIFSLB",
    name: "Universidad Nacional Intercultural Fabiola Salazar Legu\xEDa de Bagua",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#0891B2",
    type: "publica",
    sedes: [
      { id: "unifslb-bagua", name: "Campus Universitario Bagua (Av. Intercultural s/n)", city: "Amazonas" }
    ],
    carreras: [
      "Biotecnolog\xEDa",
      "Enfermer\xEDa",
      "Ingenier\xEDa de Negocios Globales",
      "Ingenier\xEDa en Acuicultura",
      "Ingenier\xEDa Zootecnista"
    ]
  },
  // 26. UNSM - Universidad Nacional de San Martín
  {
    id: "unsm",
    acronym: "UNSM",
    name: "Universidad Nacional de San Mart\xEDn",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "publica",
    sedes: [
      { id: "unsm-tarapoto", name: "Ciudad Universitaria Morales (Av. Maynas 177, Tarapoto)", city: "San Mart\xEDn" },
      { id: "unsm-moyobamba", name: "Filial Moyobamba (Jr. Callao 530)", city: "San Mart\xEDn" },
      { id: "unsm-juanjui", name: "Filial Juanju\xED (Jr. Huallaga s/n, Mariscal C\xE1ceres)", city: "San Mart\xEDn" },
      { id: "unsm-rioja", name: "Filial Rioja", city: "San Mart\xEDn" },
      { id: "unsm-tocache", name: "Filial Tocache", city: "San Mart\xEDn" },
      { id: "unsm-lamas", name: "Filial Lamas", city: "San Mart\xEDn" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Arquitectura",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Ecolog\xEDa",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Enfermer\xEDa",
      "Idiomas",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Obstetricia"
    ]
  },
  // -------------------------------------------------------------
  // 🏔️ 3. Centro del Perú (12)
  // -------------------------------------------------------------
  // 27. UNCP - Universidad Nacional del Centro del Perú
  {
    id: "uncp",
    acronym: "UNCP",
    name: "Universidad Nacional del Centro del Per\xFA",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#991B1B",
    type: "publica",
    sedes: [
      { id: "uncp-huancayo", name: "Ciudad Universitaria Huancayo (Av. Mariscal Castilla 3909, El Tambo)", city: "Jun\xEDn" },
      { id: "uncp-tarma", name: "Filial Tarma", city: "Jun\xEDn" },
      { id: "uncp-satipo", name: "Filial Satipo (R\xEDo Negro)", city: "Jun\xEDn" },
      { id: "uncp-jauja", name: "Filial Jauja (El Mantaro)", city: "Jun\xEDn" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Agronom\xEDa",
      "Antropolog\xEDa",
      "Arquitectura",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Ciencias Naturales y Ambiental",
      "Educaci\xF3n Ciencias Sociales y Historia",
      "Educaci\xF3n Educaci\xF3n F\xEDsica y Psicomotricidad",
      "Educaci\xF3n Educaci\xF3n Inicial",
      "Educaci\xF3n Educaci\xF3n Primaria",
      "Educaci\xF3n Lengua, Literatura y Comunicaci\xF3n",
      "Educaci\xF3n Matem\xE1tica e Inform\xE1tica",
      "Enfermer\xEDa",
      "Filosof\xEDa, Ciencias Sociales y Relaciones Humanas",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agr\xF3noma y Tropical",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Electr\xF3nica y Electrot\xE9cnica",
      "Ingenier\xEDa Forestal y del Medio Ambiente",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Metal\xFArgica y de Materiales",
      "Ingenier\xEDa Qu\xEDmica",
      "Ingenier\xEDa Qu\xEDmica Ambiental",
      "Ingenier\xEDa Qu\xEDmica Industrial",
      "Medicina Humana",
      "Medicina Veterinaria y Zootecnia",
      "Sociolog\xEDa",
      "Trabajo Social",
      "Zootecnia"
    ]
  },
  // 28. UNAAT - Universidad Nacional Autónoma Altoandina de Tarma
  {
    id: "unaat",
    acronym: "UNAAT",
    name: "Universidad Nacional Aut\xF3noma Altoandina de Tarma",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "publica",
    sedes: [
      { id: "unaat-tarma-central", name: "Campus Central (Av. Pacheco 325, Tarma)", city: "Jun\xEDn" },
      { id: "unaat-huaguapo", name: "Campus Huaguapo (Carretera Tarma - La Oroya Km 4.5)", city: "Jun\xEDn" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial"
    ]
  },
  // 29. UNISCJSA - Universidad Nacional Intercultural de la Selva Central Juan Santos Atahualpa
  {
    id: "uniscjsa",
    acronym: "UNISCJSA",
    name: "Universidad Nacional Intercultural de la Selva Central Juan Santos Atahualpa",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#047857",
    type: "publica",
    sedes: [
      { id: "uniscjsa-pichanaqui", name: "Sede Pichanaqui (Chanchamayo)", city: "Jun\xEDn" },
      { id: "uniscjsa-la-merced", name: "Sede La Merced (Chanchamayo)", city: "Jun\xEDn" },
      { id: "uniscjsa-satipo", name: "Sede Satipo", city: "Jun\xEDn" }
    ],
    carreras: [
      "Administraci\xF3n de Negocios Interculturales",
      "Educaci\xF3n Intercultural Biling\xFCe: Nivel Inicial",
      "Educaci\xF3n Intercultural Biling\xFCe: Nivel Primaria",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil"
    ]
  },
  // 30. UNHEVAL - Universidad Nacional Hermilio Valdizán
  {
    id: "unheval",
    acronym: "UNHEVAL",
    name: "Universidad Nacional Hermilio Valdiz\xE1n",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "publica",
    sedes: [
      { id: "unheval-huanuco", name: "Campus Universitario Cayhuayna (Av. Universitaria 601, Pillco Marca)", city: "Hu\xE1nuco" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Ciencias de la Comunicaci\xF3n Social",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Biolog\xEDa, Qu\xEDmica y Ciencia Ambiente",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico Sociales y Turismo",
      "Educaci\xF3n Secundaria en Filosof\xEDa, Psicolog\xEDa y Ciencias Sociales",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Lengua Extranjera: Ingl\xE9s - Franc\xE9s",
      "Educaci\xF3n Secundaria en Matem\xE1tica y F\xEDsica",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Industrial",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Odontolog\xEDa",
      "Psicolog\xEDa",
      "Sociolog\xEDa"
    ]
  },
  // 31. UNAS - Universidad Nacional Agraria de la Selva
  {
    id: "unas",
    acronym: "UNAS",
    name: "Universidad Nacional Agraria de la Selva",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#2D6A4F",
    type: "publica",
    sedes: [
      { id: "unas-tingo-maria", name: "Campus Central Tingo Mar\xEDa (Av. Universitaria s/n, Rupa Rupa)", city: "Hu\xE1nuco" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Contabilidad",
      "Econom\xEDa",
      "Ingenier\xEDa Agron\xF3mica",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa de Computaci\xF3n e Inform\xE1tica",
      "Ingenier\xEDa en Conservaci\xF3n de Suelos y Agua",
      "Ingenier\xEDa en Industrias Alimentarias",
      "Ingenier\xEDa en Inform\xE1tica y Sistemas",
      "Ingenier\xEDa Forestal",
      "Ingenier\xEDa Mec\xE1nica El\xE9ctrica",
      "Zootecnia"
    ]
  },
  // 32. UNDAR - Universidad Nacional Daniel Alomía Robles
  {
    id: "undar",
    acronym: "UNDAR",
    name: "Universidad Nacional Daniel Alom\xEDa Robles",
    logo: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=120&auto=format&fit=crop&q=80",
    color: "#7E22CE",
    type: "publica",
    sedes: [
      { id: "undar-huanuco-central", name: "Campus Principal (Jr. General Prado 634)", city: "Hu\xE1nuco" }
    ],
    carreras: [
      "Educaci\xF3n Musical y Artes Pl\xE1sticas",
      "Ejecuci\xF3n Musical"
    ]
  },
  // 33. UNDAC - Universidad Nacional Daniel Alcides Carrión
  {
    id: "undac",
    acronym: "UNDAC",
    name: "Universidad Nacional Daniel Alcides Carri\xF3n",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#D97706",
    type: "publica",
    sedes: [
      { id: "undac-cerro-de-pasco", name: "Campus Central San Juan (Av. Los Incas s/n, Yanacancha)", city: "Pasco" },
      { id: "undac-oxapampa", name: "Filial Oxapampa (Jr. Los Sauces s/n)", city: "Pasco" },
      { id: "undac-yanahuanca", name: "Filial Yanahuanca", city: "Pasco" },
      { id: "undac-la-merced", name: "Filial La Merced (Chanchamayo)", city: "Jun\xEDn" },
      { id: "undac-tarma", name: "Filial Tarma", city: "Jun\xEDn" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Biolog\xEDa y Qu\xEDmica",
      "Educaci\xF3n Secundaria en Ciencias Hist\xF3rico Sociales",
      "Educaci\xF3n Secundaria en Lengua y Literatura",
      "Educaci\xF3n Secundaria en Lenguas Extranjeras: Ingl\xE9s - Franc\xE9s",
      "Educaci\xF3n Secundaria en Tecnolog\xEDa e Inform\xE1tica",
      "Enfermer\xEDa",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas y Computaci\xF3n",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Zootecnista",
      "Medicina Humana",
      "Obstetricia",
      "Odontolog\xEDa"
    ]
  },
  // 34. UNH - Universidad Nacional de Huancavelica
  {
    id: "unh",
    acronym: "UNH",
    name: "Universidad Nacional de Huancavelica",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#0369A1",
    type: "publica",
    sedes: [
      { id: "unh-paturpampa", name: "Campus Paturpampa (Av. Evitamiento s/n)", city: "Huancavelica" },
      { id: "unh-lircay", name: "Filial Lircay (Angaraes)", city: "Huancavelica" },
      { id: "unh-acobamba", name: "Filial Acobamba", city: "Huancavelica" },
      { id: "unh-tayacaja", name: "Filial Tayacaja (Pampas)", city: "Huancavelica" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Educaci\xF3n Especial",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria en Ciencias Sociales y Desarrollo Rural",
      "Educaci\xF3n Secundaria en Lengua Literatura y Comunicaci\xF3n",
      "Educaci\xF3n Secundaria en Matem\xE1tica, Computaci\xF3n e Inform\xE1tica",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental y Sanitaria",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa Electr\xF3nica",
      "Obstetricia",
      "Zootecnia"
    ]
  },
  // 35. UNAT - Universidad Nacional Autónoma de Tayacaja Daniel Hernández Morillo
  {
    id: "unat",
    acronym: "UNAT",
    name: "Universidad Nacional Aut\xF3noma de Tayacaja Daniel Hern\xE1ndez Morillo",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "publica",
    sedes: [
      { id: "unat-pampas", name: "Campus Pampas Tayacaja (Jr. Grau 409, Pampas)", city: "Huancavelica" }
    ],
    carreras: [
      "Enfermer\xEDa",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Forestal y Ambiental",
      "Ingenier\xEDa Industrial"
    ]
  },
  // 36. UNSCH - Universidad Nacional de San Cristóbal de Huamanga
  {
    id: "unsch",
    acronym: "UNSCH",
    name: "Universidad Nacional de San Crist\xF3bal de Huamanga",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#7C2D12",
    type: "publica",
    sedes: [
      { id: "unsch-ayacucho", name: "Campus Terrazas de Ayacucho (Av. Independencia s/n, Huamanga)", city: "Ayacucho" },
      { id: "unsch-pichari", name: "Filial Pichari (VRAEM, La Convenci\xF3n)", city: "Cusco" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Agronom\xEDa",
      "Antropolog\xEDa Social",
      "Arqueolog\xEDa",
      "Biolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad y Auditor\xEDa",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroforestal",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Qu\xEDmica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Obstetricia",
      "Trabajo Social",
      "Zootecnia"
    ]
  },
  // 37. UNAH - Universidad Nacional Autónoma de Huanta
  {
    id: "unah",
    acronym: "UNAH",
    name: "Universidad Nacional Aut\xF3noma de Huanta",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#3B82F6",
    type: "publica",
    sedes: [
      { id: "unah-huanta-central", name: "Campus Central Huanta (Jr. Razuhuillca 624)", city: "Ayacucho" }
    ],
    carreras: [
      "Administraci\xF3n de Turismo y Hoteler\xEDa",
      "Ingenier\xEDa de Negocios Agron\xF3micos y Forestales",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa en Bioprocesos Industriales"
    ]
  },
  // 38. UNICA - Universidad Nacional San Luis Gonzaga
  {
    id: "unica",
    acronym: "UNICA",
    name: "Universidad Nacional San Luis Gonzaga",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "publica",
    sedes: [
      { id: "unica-ica", name: "Ciudad Universitaria (Av. Los Maestros s/n)", city: "Ica" },
      { id: "unica-chincha", name: "Filial Chincha (Calle Grocio Prado s/n)", city: "Ica" },
      { id: "unica-nasca", name: "Filial Nasca (Av. Los Incas s/n)", city: "Ica" },
      { id: "unica-pisco", name: "Filial Pisco (San Clemente)", city: "Ica" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Arqueolog\xEDa",
      "Arquitectura",
      "Biolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Art\xEDstica",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Estomatolog\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "F\xEDsica",
      "Historia",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica y El\xE9ctrica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1tica e Inform\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria y Zootecnia",
      "Obstetricia",
      "Odontolog\xEDa",
      "Psicolog\xEDa",
      "Sociolog\xEDa",
      "Tecnolog\xEDa M\xE9dica",
      "Turismo"
    ]
  },
  // -------------------------------------------------------------
  // 🦅 4. Sur del Perú (9)
  // -------------------------------------------------------------
  // 39. UNSA - Universidad Nacional de San Agustín de Arequipa
  {
    id: "unsa",
    acronym: "UNSA",
    name: "Universidad Nacional de San Agust\xEDn de Arequipa",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#800000",
    type: "publica",
    sedes: [
      { id: "unsa-independencia", name: "Campus Ingenier\xEDas (Av. Independencia s/n)", city: "Arequipa" },
      { id: "unsa-biomedicas", name: "Campus Biom\xE9dicas (Av. Alcides Carri\xF3n s/n)", city: "Arequipa" },
      { id: "unsa-sociales", name: "Campus Sociales (Av. Venezuela s/n)", city: "Arequipa" },
      { id: "unsa-camana", name: "Filial Caman\xE1 (El Cardo)", city: "Arequipa" },
      { id: "unsa-mollendo", name: "Filial Mollendo (Islay)", city: "Arequipa" },
      { id: "unsa-majes", name: "Filial Majes / Pedregal (Caylloma)", city: "Arequipa" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Antropolog\xEDa",
      "Arquitectura",
      "Artes con menci\xF3n en Canto, Danza, M\xFAsica y Pl\xE1sticas",
      "Banca y Seguros",
      "Biolog\xEDa",
      "Ciencia de la Computaci\xF3n",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Finanzas",
      "F\xEDsica",
      "Geograf\xEDa",
      "Historia",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Industria Alimentaria",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa de Telecomunicaciones",
      "Ingenier\xEDa El\xE9ctrica",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Geof\xEDsica",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Ingenier\xEDa Sanitaria",
      "Literatura y Ling\xFC\xEDstica",
      "Matem\xE1ticas",
      "Medicina Humana",
      "Nutrici\xF3n Humana",
      "Psicolog\xEDa",
      "Qu\xEDmica",
      "Relaciones Industriales",
      "Sociolog\xEDa",
      "Trabajo Social",
      "Turismo y Hoteler\xEDa"
    ]
  },
  // 40. UNSAAC - Universidad Nacional de San Antonio Abad del Cusco
  {
    id: "unsaac",
    acronym: "UNSAAC",
    name: "Universidad Nacional de San Antonio Abad del Cusco",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#7C2D12",
    type: "publica",
    sedes: [
      { id: "unsaac-cusco-perayoc", name: "Campus Universitario Perayoc (Av. de la Cultura 733)", city: "Cusco" },
      { id: "unsaac-canchis", name: "Filial Sicuani (Canchis)", city: "Cusco" },
      { id: "unsaac-chumbivilcas", name: "Filial Santo Tom\xE1s (Chumbivilcas)", city: "Cusco" },
      { id: "unsaac-espinar", name: "Filial Yauri (Espinar)", city: "Cusco" },
      { id: "unsaac-la-convencion", name: "Filial Quillabamba (La Convenci\xF3n)", city: "Cusco" },
      { id: "unsaac-andahuaylas", name: "Filial Andahuaylas", city: "Apur\xEDmac" },
      { id: "unsaac-puerto-maldonado", name: "Filial Puerto Maldonado (Ingenier\xEDa Forestal)", city: "Madre de Dios" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Agronom\xEDa Tropical",
      "Antropolog\xEDa",
      "Arqueolog\xEDa",
      "Arquitectura",
      "Biolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "F\xEDsica",
      "Historia",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa El\xE9ctrica",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Inform\xE1tica y de Sistemas",
      "Ingenier\xEDa Mec\xE1nica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Petroqu\xEDmica",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Obstetricia",
      "Odontolog\xEDa",
      "Psicolog\xEDa",
      "Qu\xEDmica",
      "Zootecnia"
    ]
  },
  // 41. UNIQ - Universidad Nacional Intercultural de Quillabamba
  {
    id: "uniq",
    acronym: "UNIQ",
    name: "Universidad Nacional Intercultural de Quillabamba",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#059669",
    type: "publica",
    sedes: [
      { id: "uniq-quillabamba", name: "Campus El Pintobamba (Av. Universitaria s/n, La Convenci\xF3n)", city: "Cusco" }
    ],
    carreras: [
      "Eco Negocios Globales",
      "Ingenier\xEDa Agron\xF3mica Tropical",
      "Ingenier\xEDa de Alimentos",
      "Ingenier\xEDa Ecotur\xEDstica"
    ]
  },
  // 42. UNAP - Universidad Nacional del Altiplano (Puno)
  {
    id: "unap-puno",
    acronym: "UNAP",
    name: "Universidad Nacional del Altiplano",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "publica",
    sedes: [
      { id: "unap-puno-central", name: "Ciudad Universitaria (Av. Sesquicentenario s/n, Puno)", city: "Puno" },
      { id: "unap-chucuito", name: "Filial Chucuito (Desaguadero)", city: "Puno" },
      { id: "unap-azangaro", name: "Filial Az\xE1ngaro", city: "Puno" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Antropolog\xEDa",
      "Arquitectura y Urbanismo",
      "Arte",
      "Biolog\xEDa",
      "Ciencias de la Comunicaci\xF3n Social",
      "Contabilidad",
      "Derecho",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "F\xEDsico Matem\xE1tica",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Comercial",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Econ\xF3mica",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Geol\xF3gica",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Qu\xEDmica",
      "Ingenier\xEDa Topogr\xE1fica y Agrimensura",
      "Medicina Humana",
      "Medicina Veterinaria y Zootecnia",
      "Nutrici\xF3n Humana",
      "Odontolog\xEDa",
      "Sociolog\xEDa",
      "Trabajo Social",
      "Turismo"
    ]
  },
  // 43. UNAJ - Universidad Nacional de Juliaca
  {
    id: "unaj",
    acronym: "UNAJ",
    name: "Universidad Nacional de Juliaca",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#D97706",
    type: "publica",
    sedes: [
      { id: "unaj-juliaca-central", name: "Campus Taparachi (Av. Nueva Zelandia 631, Juliaca)", city: "Puno" },
      { id: "unaj-ayabacas", name: "Campus Ayabacas (Carretera Puno - Juliaca Km 5)", city: "Puno" }
    ],
    carreras: [
      "Gesti\xF3n P\xFAblica y Social",
      "Ingenier\xEDa Ambiental y Forestal",
      "Ingenier\xEDa de mecatr\xF3nica",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Software y Sistemas",
      "Ingenier\xEDa en Enolog\xEDa y Viticultura",
      "Ingenier\xEDa en Industrias Alimentarias",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Textil y de Confecciones"
    ]
  },
  // 44. UNAMBA - Universidad Nacional Micaela Bastidas de Apurímac
  {
    id: "unamba",
    acronym: "UNAMBA",
    name: "Universidad Nacional Micaela Bastidas de Apur\xEDmac",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#C2410C",
    type: "publica",
    sedes: [
      { id: "unamba-abancay", name: "Campus Tamburco (Av. Arenas 121, Abancay)", city: "Apur\xEDmac" },
      { id: "unamba-haquira", name: "Filial Haquira (Cotabambas)", city: "Apur\xEDmac" },
      { id: "unamba-vilcabamba", name: "Filial Vilcabamba (Grau)", city: "Apur\xEDmac" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Educaci\xF3n Inicial Intercultural Biling\xFCe",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agroecol\xF3gica y Desarrollo Rural",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa Inform\xE1tica y Sistemas",
      "Medicina Veterinaria y Zootecnia"
    ]
  },
  // 45. UNAJMA - Universidad Nacional José María Arguedas
  {
    id: "unajma",
    acronym: "UNAJMA",
    name: "Universidad Nacional Jos\xE9 Mar\xEDa Arguedas",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "publica",
    sedes: [
      { id: "unajma-andahuaylas", name: "Campus San Jer\xF3nimo (Av. Per\xFA s/n, Andahuaylas)", city: "Apur\xEDmac" }
    ],
    carreras: [
      "Administraci\xF3n de Empresas",
      "Contabilidad",
      "Educaci\xF3n Primaria Intercultural Biling\xFCe",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  // 46. UNAM - Universidad Nacional de Moquegua
  {
    id: "unam",
    acronym: "UNAM",
    name: "Universidad Nacional de Moquegua",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#047857",
    type: "publica",
    sedes: [
      { id: "unam-moquegua", name: "Campus Universitario Moquegua (Calle Ancash s/n)", city: "Moquegua" },
      { id: "unam-ilo", name: "Filial Ilo (Pampa Inal\xE1mbrica)", city: "Moquegua" },
      { id: "unam-ichuna", name: "Filial Ichu\xF1a (General S\xE1nchez Cerro)", city: "Moquegua" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Contabilidad",
      "Gesti\xF3n P\xFAblica y Desarrollo Social",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa Pesquera",
      "Medicina del Deporte"
    ]
  },
  // 47. UNJBG - Universidad Nacional Jorge Basadre Grohmann
  {
    id: "unjbg",
    acronym: "UNJBG",
    name: "Universidad Nacional Jorge Basadre Grohmann",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "publica",
    sedes: [
      { id: "unjbg-citos", name: "Campus Citos (Av. Miraflores s/n, Tacna)", city: "Tacna" },
      { id: "unjbg-los-granados", name: "Campus Los Granados", city: "Tacna" }
    ],
    carreras: [
      "Agronom\xEDa",
      "Artes",
      "Biolog\xEDa - Microbiolog\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa Agraria",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "F\xEDsica",
      "Historia",
      "Ingenier\xEDa Agr\xEDcola",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Comercial",
      "Ingenier\xEDa de Minas",
      "Ingenier\xEDa en Inform\xE1tica y Sistemas",
      "Ingenier\xEDa Metal\xFArgica",
      "Ingenier\xEDa Pesquera",
      "Ingenier\xEDa Qu\xEDmica",
      "Matem\xE1tica",
      "Medicina Humana",
      "Medicina Veterinaria y Zootecnia",
      "Obstetricia",
      "Odontolog\xEDa"
    ]
  },
  // -------------------------------------------------------------
  // 🌴 5. Oriente / Selva (5)
  // -------------------------------------------------------------
  // 48. UNAP - Universidad Nacional de la Amazonía Peruana (Loreto)
  {
    id: "unap-loreto",
    acronym: "UNAP",
    name: "Universidad Nacional de la Amazon\xEDa Peruana",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "publica",
    sedes: [
      { id: "unap-zungarococha", name: "Campus Zungarococha (San Juan Bautista, Iquitos)", city: "Loreto" },
      { id: "unap-maynas", name: "Campus Maynas (Calle Pucallpa 1066, Iquitos)", city: "Loreto" },
      { id: "unap-requena", name: "Filial Requena", city: "Loreto" },
      { id: "unap-nauta", name: "Filial Nauta (Loreto)", city: "Loreto" },
      { id: "unap-yurimaguas", name: "Filial Yurimaguas (Alto Amazonas)", city: "Loreto" },
      { id: "unap-caballococha", name: "Filial Caballococha (Mariscal Ram\xF3n Castilla)", city: "Loreto" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Acuicultura",
      "Antropolog\xEDa Social",
      "Biolog\xEDa",
      "Bromatolog\xEDa y Nutrici\xF3n Humana",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Ecolog\xEDa Forestal",
      "Econom\xEDa",
      "Educaci\xF3n F\xEDsica",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa Forestal",
      "Ingenier\xEDa en Ecolog\xEDa de Bosques Tropicales",
      "Ingenier\xEDa Qu\xEDmica",
      "Medicina Humana",
      "Medicina Veterinaria",
      "Negocios Internacionales y Turismo",
      "Odontolog\xEDa"
    ]
  },
  // 49. UNAAA - Universidad Nacional Autónoma de Alto Amazonas
  {
    id: "unaaa",
    acronym: "UNAAA",
    name: "Universidad Nacional Aut\xF3noma de Alto Amazonas",
    logo: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=120&auto=format&fit=crop&q=80",
    color: "#059669",
    type: "publica",
    sedes: [
      { id: "unaaa-yurimaguas", name: "Campus Yurimaguas (Calle Progresismo 507)", city: "Loreto" }
    ],
    carreras: [
      "Contabilidad",
      "Ingenier\xEDa Agr\xF3noma",
      "Ingenier\xEDa en Acuicultura",
      "Ingenier\xEDa en Agropecuaria",
      "Ingenier\xEDa Zootecnica",
      "Zootecnia"
    ]
  },
  // 50. UNU - Universidad Nacional de Ucayali
  {
    id: "unu",
    acronym: "UNU",
    name: "Universidad Nacional de Ucayali",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "publica",
    sedes: [
      { id: "unu-pucallpa", name: "Campus Pucallpa (Carretera Federico Basadre Km 6.2)", city: "Ucayali" },
      { id: "unu-aguaytia", name: "Filial Aguayt\xEDa (Padre Abad)", city: "Ucayali" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Agronom\xEDa",
      "Ciencias de la Comunicaci\xF3n",
      "Contabilidad",
      "Derecho y Ciencias Pol\xEDticas",
      "Econom\xEDa y Negocios Internacionales",
      "Educaci\xF3n Inicial",
      "Educaci\xF3n Primaria",
      "Educaci\xF3n Secundaria",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Forestal",
      "Medicina Humana"
    ]
  },
  // 51. UNIA - Universidad Nacional Intercultural de la Amazonía
  {
    id: "unia",
    acronym: "UNIA",
    name: "Universidad Nacional Intercultural de la Amazon\xEDa",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#0D9488",
    type: "publica",
    sedes: [
      { id: "unia-yarinacocha", name: "Campus Yarinacocha (Carretera Yarinacocha Km 2, Pucallpa)", city: "Ucayali" }
    ],
    carreras: [
      "Educaci\xF3n Intercultural Biling\xFCe: Nivel Inicial y Primaria",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa Agroforestal Acu\xEDcola"
    ]
  },
  // 52. UNAMAD - Universidad Nacional Amazónica de Madre de Dios
  {
    id: "unamad",
    acronym: "UNAMAD",
    name: "Universidad Nacional Amaz\xF3nica de Madre de Dios",
    logo: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=120&auto=format&fit=crop&q=80",
    color: "#166534",
    type: "publica",
    sedes: [
      { id: "unamad-puerto-maldonado", name: "Campus Puerto Maldonado (Av. Jorge Ch\xE1vez 1160)", city: "Madre de Dios" }
    ],
    carreras: [
      "Administraci\xF3n y Negocios Internacionales",
      "Contabilidad y Finanzas",
      "Derecho y Ciencias Pol\xEDticas",
      "Ecoturismo",
      "Educaci\xF3n Inicial y Especial",
      "Educaci\xF3n Matem\xE1tica y Computaci\xF3n",
      "Educaci\xF3n Primaria e Inform\xE1tica",
      "Enfermer\xEDa",
      "Ingenier\xEDa Agroindustrial",
      "Ingenier\xEDa de Sistemas e Inform\xE1tica",
      "Ingenier\xEDa Forestal y Medio Ambiente",
      "Medicina Veterinaria y Zootecnia"
    ]
  },
  // =============================================================
  // 🏢 UNIVERSIDADES PRIVADAS LICENCIADAS POR SUNEDU
  // =============================================================
  // -------------------------------------------------------------
  // 1. Las Grandes Redes Nacionales (Presencia Multirregional)
  // -------------------------------------------------------------
  {
    id: "utp",
    acronym: "UTP",
    name: "Universidad Tecnol\xF3gica del Per\xFA",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#E31E24",
    type: "privada",
    sedes: [
      { id: "lima-centro", name: "Lima Centro (Av. Arequipa)", city: "Lima" },
      { id: "lima-norte", name: "Lima Norte (Independencia)", city: "Lima" },
      { id: "lima-sur", name: "Lima Sur (Villa El Salvador)", city: "Lima" },
      { id: "sjl", name: "Lima Este (San Juan de Lurigancho)", city: "Lima" },
      { id: "ate", name: "Ate Vitarte", city: "Lima" },
      { id: "arequipa", name: "Arequipa Central", city: "Arequipa" },
      { id: "chiclayo", name: "Chiclayo", city: "Lambayeque" },
      { id: "chimbote", name: "Chimbote", city: "\xC1ncash" },
      { id: "huancayo", name: "Huancayo", city: "Jun\xEDn" },
      { id: "ica", name: "Ica", city: "Ica" },
      { id: "piura", name: "Piura", city: "Piura" },
      { id: "trujillo", name: "Trujillo", city: "La Libertad" }
    ],
    carreras: [
      "Ingenier\xEDa de Sistemas",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa de Software",
      "Administraci\xF3n",
      "Contabilidad",
      "Marketing",
      "Derecho",
      "Psicolog\xEDa",
      "Arquitectura",
      "Ciencias de la Comunicaci\xF3n"
    ]
  },
  {
    id: "ucv",
    acronym: "UCV",
    name: "Universidad C\xE9sar Vallejo",
    logo: "https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "privada",
    sedes: [
      { id: "trujillo-fundacional", name: "Sede Fundacional Trujillo", city: "La Libertad" },
      { id: "lima-norte-ucv", name: "Lima Norte (Los Olivos)", city: "Lima" },
      { id: "lima-este-sjl-ucv", name: "Lima Este (San Juan de Lurigancho)", city: "Lima" },
      { id: "ate-ucv", name: "Ate Vitarte", city: "Lima" },
      { id: "callao-ucv", name: "Callao", city: "Callao" },
      { id: "piura-ucv", name: "Piura", city: "Piura" },
      { id: "chiclayo-ucv", name: "Chiclayo", city: "Lambayeque" },
      { id: "chimbote-ucv", name: "Chimbote", city: "\xC1ncash" },
      { id: "tarapoto-ucv", name: "Tarapoto", city: "San Mart\xEDn" },
      { id: "moyobamba-ucv", name: "Moyobamba", city: "San Mart\xEDn" },
      { id: "huaraz-ucv", name: "Huaraz", city: "\xC1ncash" },
      { id: "sullana-ucv", name: "Sullana", city: "Piura" }
    ],
    carreras: [
      "Psicolog\xEDa",
      "Derecho",
      "Enfermer\xEDa",
      "Estomatolog\xEDa",
      "Ingenier\xEDa Civil",
      "Arquitectura",
      "Ingenier\xEDa de Sistemas",
      "Administraci\xF3n",
      "Educaci\xF3n",
      "Ciencias de la Comunicaci\xF3n"
    ]
  },
  {
    id: "upn",
    acronym: "UPN",
    name: "Universidad Privada del Norte",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#D97706",
    type: "privada",
    sedes: [
      { id: "trujillo-el-molino", name: "Trujillo (El Molino)", city: "La Libertad" },
      { id: "trujillo-san-isidro", name: "Trujillo (San Isidro)", city: "La Libertad" },
      { id: "cajamarca-upn", name: "Sede Cajamarca", city: "Cajamarca" },
      { id: "lima-brena", name: "Lima (Bre\xF1a)", city: "Lima" },
      { id: "lima-los-olivos-upn", name: "Lima (Los Olivos)", city: "Lima" },
      { id: "lima-sjl-upn", name: "Lima (San Juan de Lurigancho)", city: "Lima" },
      { id: "lima-comas-upn", name: "Lima (Comas)", city: "Lima" },
      { id: "lima-chorrillos-upn", name: "Lima (Chorrillos)", city: "Lima" }
    ],
    carreras: [
      "Arquitectura",
      "Ingenier\xEDa de Sistemas Computacionales",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Industrial",
      "Derecho",
      "Nutrici\xF3n",
      "Terapia F\xEDsica",
      "Psicolog\xEDa",
      "Administraci\xF3n",
      "Comunicaciones"
    ]
  },
  {
    id: "uc",
    acronym: "UC",
    name: "Universidad Continental",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#EA580C",
    type: "privada",
    sedes: [
      { id: "huancayo-central", name: "Huancayo (Sede Central)", city: "Jun\xEDn" },
      { id: "lima-los-olivos", name: "Lima (Los Olivos / Miraflores)", city: "Lima" },
      { id: "arequipa-uc", name: "Arequipa", city: "Arequipa" },
      { id: "cusco-uc", name: "Cusco", city: "Cusco" }
    ],
    carreras: [
      "Medicina Humana",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Empresarial",
      "Arquitectura",
      "Derecho",
      "Psicolog\xEDa",
      "Administraci\xF3n"
    ]
  },
  {
    id: "upeu",
    acronym: "UPeU",
    name: "Universidad Peruana Uni\xF3n",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#1D4ED8",
    type: "privada",
    sedes: [
      { id: "lima-nana", name: "Lima (\xD1a\xF1a - Lurigancho)", city: "Lima" },
      { id: "juliaca-upeu", name: "Juliaca", city: "Puno" },
      { id: "tarapoto-upeu", name: "Tarapoto", city: "San Mart\xEDn" }
    ],
    carreras: [
      "Medicina Humana",
      "Enfermer\xEDa",
      "Nutrici\xF3n",
      "Ingenier\xEDa de Sistemas",
      "Arquitectura",
      "Teolog\xEDa",
      "Administraci\xF3n"
    ]
  },
  {
    id: "ucss",
    acronym: "UCSS",
    name: "Universidad Cat\xF3lica Sedes Sapientiae",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#0F766E",
    type: "privada",
    sedes: [
      { id: "lima-norte-ucss", name: "Lima Norte (Los Olivos)", city: "Lima" },
      { id: "huaura-huacho", name: "Huaura (Huacho)", city: "Lima Provincias" },
      { id: "chulucanas-piura", name: "Chulucanas", city: "Piura" },
      { id: "atalaya-ucayali", name: "Atalaya", city: "Ucayali" },
      { id: "nueva-cajamarca", name: "Nueva Cajamarca", city: "San Mart\xEDn" },
      { id: "vraem-ucss", name: "Sede VRAEM", city: "Ayacucho" }
    ],
    carreras: [
      "Educaci\xF3n",
      "Enfermer\xEDa",
      "Psicolog\xEDa",
      "Ingenier\xEDa Agraria",
      "Contabilidad",
      "Administraci\xF3n"
    ]
  },
  // -------------------------------------------------------------
  // 2. Las Líderes de Lima (Con múltiples campus)
  // -------------------------------------------------------------
  {
    id: "upc",
    acronym: "UPC",
    name: "Universidad Peruana de Ciencias Aplicadas",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#CC0000",
    type: "privada",
    sedes: [
      { id: "monterrico-upc", name: "Campus Monterrico (Surco)", city: "Lima" },
      { id: "san-isidro-upc", name: "Campus San Isidro", city: "Lima" },
      { id: "villa-upc", name: "Campus Villa (Chorrillos)", city: "Lima" },
      { id: "san-miguel-upc", name: "Campus San Miguel", city: "Lima" }
    ],
    carreras: [
      "Medicina",
      "Odontolog\xEDa",
      "Ingenier\xEDa de Software",
      "Ciencias de la Computaci\xF3n",
      "Arquitectura",
      "Administraci\xF3n",
      "Dise\xF1o Gr\xE1fico",
      "Comunicaci\xF3n Audiovisual",
      "M\xFAsica",
      "Traducci\xF3n e Interpretaci\xF3n"
    ]
  },
  {
    id: "usil",
    acronym: "USIL",
    name: "Universidad San Ignacio de Loyola",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#0369A1",
    type: "privada",
    sedes: [
      { id: "la-molina-usil", name: "Campus La Molina", city: "Lima" },
      { id: "pachacamac-usil", name: "Campus Pachac\xE1mac", city: "Lima" }
    ],
    carreras: [
      "Gastronom\xEDa y Gesti\xF3n Culinaria",
      "Hoteler\xEDa",
      "Negocios Internacionales",
      "Marketing",
      "Ingenier\xEDa Industrial",
      "Comunicaciones"
    ]
  },
  {
    id: "ucsur",
    acronym: "UCSUR",
    name: "Universidad Cient\xEDfica del Sur",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#006B3F",
    type: "privada",
    sedes: [
      { id: "villa-chorrillos", name: "Campus Villa (Chorrillos)", city: "Lima" },
      { id: "los-olivos-norte", name: "Campus Norte (Los Olivos)", city: "Lima" }
    ],
    carreras: [
      "Medicina Humana",
      "Medicina Veterinaria",
      "Biolog\xEDa Marina",
      "Nutrici\xF3n",
      "Odontolog\xEDa",
      "Ingenier\xEDa Ambiental",
      "Artes Esc\xE9nicas"
    ]
  },
  {
    id: "upsjb",
    acronym: "UPSJB",
    name: "Universidad Privada San Juan Bautista",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "privada",
    sedes: [
      { id: "chorrillos-upsjb", name: "Lima (Chorrillos)", city: "Lima" },
      { id: "san-borja-upsjb", name: "Lima (San Borja)", city: "Lima" },
      { id: "ica-upsjb", name: "Sede Ica", city: "Ica" },
      { id: "chincha-upsjb", name: "Filial Chincha", city: "Ica" }
    ],
    carreras: [
      "Medicina Humana",
      "Enfermer\xEDa",
      "Estomatolog\xEDa",
      "Derecho",
      "Administraci\xF3n",
      "Ingenier\xEDa de Computaci\xF3n y Sistemas"
    ]
  },
  {
    id: "usmp",
    acronym: "USMP",
    name: "Universidad de San Mart\xEDn de Porres",
    logo: "https://images.unsplash.com/photo-1532649538693-f3a2ec1bf8bd?w=120&auto=format&fit=crop&q=80",
    color: "#1A365D",
    type: "privada",
    sedes: [
      { id: "lima-central-usmp", name: "Lima (Santa Anita / La Molina / Surquillo)", city: "Lima" },
      { id: "chiclayo-filial", name: "Filial Chiclayo", city: "Lambayeque" },
      { id: "arequipa-filial", name: "Filial Arequipa", city: "Arequipa" }
    ],
    carreras: [
      "Medicina Humana",
      "Odontolog\xEDa",
      "Derecho",
      "Ciencias de la Comunicaci\xF3n",
      "Turismo y Hoteler\xEDa",
      "Psicolog\xEDa",
      "Arquitectura"
    ]
  },
  // -------------------------------------------------------------
  // 3. Las Tradicionales y Especializadas (Sede Única en Lima)
  // -------------------------------------------------------------
  {
    id: "pucp",
    acronym: "PUCP",
    name: "Pontificia Universidad Cat\xF3lica del Per\xFA",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#002F6C",
    type: "privada",
    sedes: [
      { id: "san-miguel-pucp", name: "Campus San Miguel (Av. Universitaria)", city: "Lima" }
    ],
    carreras: [
      "Derecho",
      "Comunicaciones",
      "Psicolog\xEDa",
      "Artes Esc\xE9nicas",
      "Ingenier\xEDa Inform\xE1tica",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mec\xE1nica",
      "F\xEDsica"
    ]
  },
  {
    id: "ulima",
    acronym: "ULIMA",
    name: "Universidad de Lima",
    logo: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=120&auto=format&fit=crop&q=80",
    color: "#FF6600",
    type: "privada",
    sedes: [
      { id: "surco-monterrico", name: "Campus Surco (Av. Javier Prado)", city: "Lima" }
    ],
    carreras: [
      "Comunicaciones",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa de Sistemas",
      "Administraci\xF3n",
      "Econom\xEDa",
      "Derecho",
      "Arquitectura"
    ]
  },
  {
    id: "up",
    acronym: "UP",
    name: "Universidad del Pac\xEDfico",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#002F6C",
    type: "privada",
    sedes: [
      { id: "jesus-maria-up", name: "Campus Jes\xFAs Mar\xEDa (Av. Salaverry)", city: "Lima" }
    ],
    carreras: [
      "Econom\xEDa",
      "Finanzas",
      "Administraci\xF3n",
      "Contabilidad",
      "Ingenier\xEDa de la Informaci\xF3n"
    ]
  },
  {
    id: "utec",
    acronym: "UTEC",
    name: "Universidad de Ingenier\xEDa y Tecnolog\xEDa",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#00A3E0",
    type: "privada",
    sedes: [
      { id: "barranco-utec", name: "Campus Barranco (Av. Grau)", city: "Lima" }
    ],
    carreras: [
      "Ingenier\xEDa Ambiental",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa Electr\xF3nica",
      "Ingenier\xEDa Industrial",
      "Ingenier\xEDa Mecatr\xF3nica",
      "Ingenier\xEDa Qu\xEDmica",
      "Bioingenier\xEDa",
      "Data Science / Ciencia de Datos"
    ]
  },
  {
    id: "urp",
    acronym: "URP",
    name: "Universidad Ricardo Palma",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#047857",
    type: "privada",
    sedes: [
      { id: "surco-urp", name: "Campus Surco (Av. Benavides)", city: "Lima" }
    ],
    carreras: [
      "Arquitectura",
      "Medicina Humana",
      "Traducci\xF3n e Interpretaci\xF3n",
      "Ingenier\xEDa Civil",
      "Psicolog\xEDa"
    ]
  },
  {
    id: "uesan",
    acronym: "UESAN",
    name: "Universidad ESAN",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "privada",
    sedes: [
      { id: "surco-esan", name: "Campus Surco (Alonso de Molina)", city: "Lima" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Econom\xEDa",
      "Ingenier\xEDa Industrial",
      "Psicolog\xEDa del Consumidor"
    ]
  },
  {
    id: "uwiener",
    acronym: "UWIENER",
    name: "Universidad Norbert Wiener",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#4F46E5",
    type: "privada",
    sedes: [
      { id: "lima-centro-uwiener", name: "Campus Lima Centro (Av. Arequipa)", city: "Lima" }
    ],
    carreras: [
      "Enfermer\xEDa",
      "Obstetricia",
      "Farmacia y Bioqu\xEDmica",
      "Odontolog\xEDa",
      "Tecnolog\xEDa M\xE9dica"
    ]
  },
  {
    id: "upch",
    acronym: "UPCH",
    name: "Universidad Peruana Cayetano Heredia",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "privada",
    sedes: [
      { id: "smp-medica", name: "San Mart\xEDn de Porres (Sede Central M\xE9dica)", city: "Lima" },
      { id: "la-molina-upch", name: "La Molina (Veterinaria y Biolog\xEDa)", city: "Lima" }
    ],
    carreras: [
      "Medicina Humana",
      "Biolog\xEDa",
      "Medicina Veterinaria",
      "Estomatolog\xEDa / Odontolog\xEDa",
      "Nutrici\xF3n"
    ]
  },
  {
    id: "ucal",
    acronym: "UCAL",
    name: "Universidad de Ciencias y Artes de Am\xE9rica Latina",
    logo: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=120&auto=format&fit=crop&q=80",
    color: "#EC4899",
    type: "privada",
    sedes: [
      { id: "la-molina-ucal", name: "Campus La Molina", city: "Lima" }
    ],
    carreras: [
      "Arquitectura",
      "Dise\xF1o Gr\xE1fico",
      "Comunicaci\xF3n Audiovisual"
    ]
  },
  {
    id: "unife",
    acronym: "UNIF\xC9",
    name: "Universidad Femenina del Sagrado Coraz\xF3n",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#8B5CF6",
    type: "privada",
    sedes: [
      { id: "la-molina-unife", name: "Campus La Molina", city: "Lima" }
    ],
    carreras: [
      "Psicolog\xEDa",
      "Derecho",
      "Educaci\xF3n",
      "Arquitectura",
      "Ingenier\xEDa de Sistemas",
      "Traducci\xF3n e Interpretaci\xF3n",
      "Nutrici\xF3n"
    ]
  },
  {
    id: "uarm",
    acronym: "UARM",
    name: "Universidad Antonio Ruiz de Montoya",
    logo: "https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=120&auto=format&fit=crop&q=80",
    color: "#0D9488",
    type: "privada",
    sedes: [
      { id: "pueblo-libre-uarm", name: "Campus Pueblo Libre", city: "Lima" }
    ],
    carreras: [
      "Filosof\xEDa",
      "Educaci\xF3n",
      "Periodismo",
      "Psicolog\xEDa",
      "Ingenier\xEDa Industrial",
      "Derecho"
    ]
  },
  // -------------------------------------------------------------
  // 4. Gigantes Regionales Privadas
  // -------------------------------------------------------------
  {
    id: "udep",
    acronym: "UDEP",
    name: "Universidad de Piura",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#003366",
    type: "privada",
    sedes: [
      { id: "piura-central", name: "Campus Piura (Sede Central)", city: "Piura" },
      { id: "miraflores-lima", name: "Campus Lima (Miraflores)", city: "Lima" }
    ],
    carreras: [
      "Ingenier\xEDa Industrial y de Sistemas",
      "Direcci\xF3n de Empresas",
      "Econom\xEDa",
      "Comunicaci\xF3n",
      "Derecho",
      "Educaci\xF3n"
    ]
  },
  {
    id: "upao",
    acronym: "UPAO",
    name: "Universidad Privada Antenor Orrego",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "privada",
    sedes: [
      { id: "trujillo-central", name: "Sede Central Trujillo", city: "La Libertad" },
      { id: "piura-filial", name: "Filial Piura", city: "Piura" }
    ],
    carreras: [
      "Medicina Humana",
      "Arquitectura",
      "Ciencias de la Comunicaci\xF3n",
      "Derecho",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  {
    id: "ucsm",
    acronym: "UCSM",
    name: "Universidad Cat\xF3lica de Santa Mar\xEDa",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#0369A1",
    type: "privada",
    sedes: [
      { id: "arequipa-umacollo", name: "Sede Arequipa (Umacollo)", city: "Arequipa" }
    ],
    carreras: [
      "Medicina",
      "Odontolog\xEDa",
      "Ingenier\xEDa Industrial",
      "Arquitectura",
      "Farmacia y Bioqu\xEDmica",
      "Derecho"
    ]
  },
  {
    id: "ucsp",
    acronym: "UCSP",
    name: "Universidad Cat\xF3lica San Pablo",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#1E40AF",
    type: "privada",
    sedes: [
      { id: "arequipa-san-lazaro", name: "Sede Arequipa (San L\xE1zaro)", city: "Arequipa" }
    ],
    carreras: [
      "Ciencia de la Computaci\xF3n",
      "Ingenier\xEDa Industrial",
      "Administraci\xF3n de Empresas",
      "Derecho",
      "Psicolog\xEDa"
    ]
  },
  {
    id: "uac",
    acronym: "UAC",
    name: "Universidad Andina del Cusco",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#B45309",
    type: "privada",
    sedes: [
      { id: "cusco-uac-central", name: "Cusco (Sede Central)", city: "Cusco" },
      { id: "quillabamba-uac", name: "Filial Quillabamba", city: "Cusco" },
      { id: "puerto-maldonado-uac", name: "Filial Puerto Maldonado", city: "Madre de Dios" }
    ],
    carreras: [
      "Medicina",
      "Derecho",
      "Arquitectura",
      "Estomatolog\xEDa",
      "Ingenier\xEDa Civil"
    ]
  },
  // -------------------------------------------------------------
  // 5. Privadas en Lima (Medianas y Especializadas)
  // -------------------------------------------------------------
  {
    id: "autonoma",
    acronym: "AUT\xD3NOMA",
    name: "Universidad Aut\xF3noma del Per\xFA",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "privada",
    sedes: [
      { id: "villa-el-salvador-autonoma", name: "Campus Villa El Salvador", city: "Lima" }
    ],
    carreras: [
      "Administraci\xF3n",
      "Ingenier\xEDa de Sistemas",
      "Arquitectura",
      "Derecho",
      "Psicolog\xEDa"
    ]
  },
  {
    id: "uch",
    acronym: "UCH",
    name: "Universidad de Ciencias y Humanidades",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#059669",
    type: "privada",
    sedes: [
      { id: "los-olivos-uch", name: "Campus Los Olivos", city: "Lima" }
    ],
    carreras: [
      "Enfermer\xEDa",
      "Educaci\xF3n",
      "Ingenier\xEDa de Sistemas",
      "Contabilidad"
    ]
  },
  {
    id: "umch",
    acronym: "UMCH",
    name: "Universidad Marcelino Champagnat",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#4338CA",
    type: "privada",
    sedes: [
      { id: "surco-umch", name: "Campus Surco", city: "Lima" }
    ],
    carreras: [
      "Educaci\xF3n Inicial y Primaria",
      "Psicolog\xEDa",
      "Administraci\xF3n",
      "Contabilidad"
    ]
  },
  {
    id: "bausate",
    acronym: "BAUSATE",
    name: "Universidad Jaime Bausate y Meza",
    logo: "https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?w=120&auto=format&fit=crop&q=80",
    color: "#DC2626",
    type: "privada",
    sedes: [
      { id: "jesus-maria-bausate", name: "Campus Jes\xFAs Mar\xEDa", city: "Lima" }
    ],
    carreras: [
      "Periodismo",
      "Comunicaci\xF3n Audiovisual"
    ]
  },
  {
    id: "cordonbleu",
    acronym: "ULCB",
    name: "Universidad Le Cordon Bleu",
    logo: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=120&auto=format&fit=crop&q=80",
    color: "#854D0E",
    type: "privada",
    sedes: [
      { id: "magdalena-ulcb", name: "Campus Magdalena del Mar", city: "Lima" }
    ],
    carreras: [
      "Gastronom\xEDa y Arte Culinario",
      "Nutrici\xF3n y T\xE9cnicas Alimentarias",
      "Ingenier\xEDa en Industrias Alimentarias",
      "Administraci\xF3n de Negocios Hoteleros y Tur\xEDsticos"
    ]
  },
  {
    id: "uma",
    acronym: "UMA",
    name: "Universidad Mar\xEDa Auxiliadora",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#7E22CE",
    type: "privada",
    sedes: [
      { id: "sjl-uma", name: "Campus San Juan de Lurigancho", city: "Lima" }
    ],
    carreras: [
      "Farmacia y Bioqu\xEDmica",
      "Enfermer\xEDa",
      "Nutrici\xF3n y Diet\xE9tica",
      "Psicolog\xEDa"
    ]
  },
  {
    id: "upal",
    acronym: "UPAL",
    name: "Universidad Privada Peruano Alemana",
    logo: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=120&auto=format&fit=crop&q=80",
    color: "#2563EB",
    type: "privada",
    sedes: [
      { id: "chorrillos-upal", name: "Campus Chorrillos", city: "Lima" }
    ],
    carreras: [
      "Empresa y Tecnolog\xEDa",
      "Ingenier\xEDa de Software"
    ]
  },
  {
    id: "ftpcl",
    acronym: "FTPCL",
    name: "Facultad de Teolog\xEDa Pontificia y Civil de Lima",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#78350F",
    type: "privada",
    sedes: [
      { id: "pueblo-libre-ftpcl", name: "Campus Pueblo Libre", city: "Lima" }
    ],
    carreras: [
      "Teolog\xEDa",
      "Filosof\xEDa",
      "Educaci\xF3n Religiosa"
    ]
  },
  // -------------------------------------------------------------
  // 6. Privadas Regionales (Fuera de Lima)
  // -------------------------------------------------------------
  {
    id: "usat",
    acronym: "USAT",
    name: "Universidad Cat\xF3lica Santo Toribio de Mogrovejo",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#0369A1",
    type: "privada",
    sedes: [
      { id: "chiclayo-usat", name: "Sede Chiclayo", city: "Lambayeque" }
    ],
    carreras: [
      "Medicina Humana",
      "Odontolog\xEDa",
      "Arquitectura",
      "Derecho",
      "Ingenier\xEDa Civil y Ambiental",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  {
    id: "uss",
    acronym: "USS",
    name: "Universidad Se\xF1or de Sip\xE1n",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#0284C7",
    type: "privada",
    sedes: [
      { id: "chiclayo-uss", name: "Sede Chiclayo (Pimentel)", city: "Lambayeque" }
    ],
    carreras: [
      "Medicina",
      "Arquitectura",
      "Estomatolog\xEDa",
      "Ingenier\xEDa Civil",
      "Derecho"
    ]
  },
  {
    id: "upla",
    acronym: "UPLA",
    name: "Universidad Peruana Los Andes",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#C2410C",
    type: "privada",
    sedes: [
      { id: "huancayo-upla", name: "Huancayo (Sede Central)", city: "Jun\xEDn" },
      { id: "chanchamayo-upla", name: "Filial Chanchamayo (La Merced)", city: "Jun\xEDn" }
    ],
    carreras: [
      "Medicina Humana",
      "Odontolog\xEDa",
      "Derecho",
      "Ingenier\xEDa Civil",
      "Arquitectura"
    ]
  },
  {
    id: "udh",
    acronym: "UDH",
    name: "Universidad de Hu\xE1nuco",
    logo: "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=120&auto=format&fit=crop&q=80",
    color: "#15803D",
    type: "privada",
    sedes: [
      { id: "huanuco-udh", name: "Hu\xE1nuco (Sede Central)", city: "Hu\xE1nuco" },
      { id: "tingo-maria-udh", name: "Filial Tingo Mar\xEDa", city: "Hu\xE1nuco" }
    ],
    carreras: [
      "Odontolog\xEDa",
      "Derecho",
      "Ingenier\xEDa Civil",
      "Enfermer\xEDa"
    ]
  },
  {
    id: "upt",
    acronym: "UPT",
    name: "Universidad Privada de Tacna",
    logo: "https://images.unsplash.com/photo-1562774053-701939374585?w=120&auto=format&fit=crop&q=80",
    color: "#B91C1C",
    type: "privada",
    sedes: [
      { id: "tacna-upt", name: "Sede Tacna (Citos)", city: "Tacna" }
    ],
    carreras: [
      "Medicina Humana",
      "Arquitectura",
      "Derecho",
      "Ingenier\xEDa Civil",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  {
    id: "lasalle",
    acronym: "LA SALLE",
    name: "Universidad La Salle",
    logo: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=120&auto=format&fit=crop&q=80",
    color: "#1E3A8A",
    type: "privada",
    sedes: [
      { id: "arequipa-lasalle", name: "Sede Arequipa", city: "Arequipa" }
    ],
    carreras: [
      "Derecho",
      "Administraci\xF3n y Negocios Internacionales",
      "Ingenier\xEDa de Software"
    ]
  },
  {
    id: "uai",
    acronym: "UAI",
    name: "Universidad Aut\xF3noma de Ica",
    logo: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=120&auto=format&fit=crop&q=80",
    color: "#0891B2",
    type: "privada",
    sedes: [
      { id: "chincha-uai", name: "Sede Chincha (Ica)", city: "Ica" }
    ],
    carreras: [
      "Enfermer\xEDa",
      "Administraci\xF3n de Empresas",
      "Ingenier\xEDa de Sistemas"
    ]
  },
  {
    id: "roosevelt",
    acronym: "ROOSEVELT",
    name: "Universidad Privada de Huancayo Franklin Roosevelt",
    logo: "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=120&auto=format&fit=crop&q=80",
    color: "#BE123C",
    type: "privada",
    sedes: [
      { id: "huancayo-roosevelt", name: "Sede Huancayo", city: "Jun\xEDn" }
    ],
    carreras: [
      "Enfermer\xEDa",
      "Farmacia y Bioqu\xEDmica",
      "Obstetricia",
      "Estomatolog\xEDa"
    ]
  }
];

// src/data/materialGeneral.ts
var UNI_GENERAL_ID = "general";

// src/data/canalesAcademias.ts
var CANALES_ACADEMIAS = [
  {
    // Página del canal: «PAMER ACADEMIAS» (sin descripción).
    id: "pamer-canal",
    academiaId: "pamer",
    nombre: "PAMER Academias (canal)",
    url: "https://whatsapp.com/channel/0029Vb6E8DiLY6d2Nql4zc3B",
    fuente: "https://pamer.edu.pe/academias",
    detalle: "Canal de WhatsApp de la academia Pamer, enlazado desde su propia web (pamer.edu.pe/academias). Avisos para postulantes y alumnos.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Página del canal: «Academia Aiapaec» (sin descripción).
    id: "aiapaec-canal",
    academiaId: "aiapaec",
    nombre: "Academia Aiapaec (canal)",
    url: "https://whatsapp.com/channel/0029VbAxgrR3AzNVC3BnoO0W",
    fuente: "https://www.academiaaiapaec.edu.pe/",
    detalle: "Canal de WhatsApp de la academia Aiapaec, enlazado desde su propia web (academiaaiapaec.edu.pe). Avisos para postulantes y alumnos.",
    revisado: "10 de octubre de 2026"
  }
];

// src/data/canalesEstado.ts
var CANALES_ESTADO = [
  {
    // Botón «Únete a nuestro canal de WhatsApp» de su Linktree oficial. Página del canal: «Pronabec», 60 mil seguidores.
    id: "pronabec-canal",
    nombre: "Pronabec (canal oficial)",
    url: "https://whatsapp.com/channel/0029VamBHHc8F2pIBPfpn634",
    fuente: "https://linktr.ee/pronabec",
    administra: "el Pronabec (Ministerio de Educaci\xF3n)",
    tema: "Becas",
    detalle: "Canal oficial del Programa Nacional de Becas: convocatorias de becas y cr\xE9ditos educativos para estudiar en el Per\xFA y el extranjero.",
    revisado: "20 de octubre de 2026"
  },
  {
    // Lo enlaza juventud.gob.pe (web oficial de la Senaju). Página del canal: «Senaju Perú», 6 100 seguidores.
    id: "senaju-canal",
    nombre: "Senaju Per\xFA (canal oficial)",
    url: "https://whatsapp.com/channel/0029Vam1Gi19WtC2b3B0vS0A",
    fuente: "https://juventud.gob.pe/",
    administra: "la Secretar\xEDa Nacional de la Juventud (Senaju)",
    tema: "Oportunidades",
    detalle: "Canal oficial de la Secretar\xEDa Nacional de la Juventud: servicios, voluntariados, concursos y oportunidades para j\xF3venes.",
    revisado: "20 de octubre de 2026"
  },
  {
    // Lo publica El Peruano (diario oficial) en la nota del MTPE sobre sus canales. Página del canal: «Ministerio de Trabajo y Promoción del Empleo», 61 mil seguidores.
    id: "mtpe-canal",
    nombre: "Ministerio de Trabajo (canal oficial)",
    url: "https://whatsapp.com/channel/0029Va0XpmpJuyAFn84DbM3H",
    fuente: "https://elperuano.pe/noticia/298371-atencion-mtpe-potencia-sus-canales-en-whatsapp-y-linkedin-para-conectar-a-peruanos-con-el-mercado-laboral",
    administra: "el Ministerio de Trabajo y Promoci\xF3n del Empleo",
    tema: "Empleo",
    detalle: "Canal oficial del MTPE: convocatorias laborales, ferias de empleo, capacitaciones gratuitas y consejos para buscar trabajo.",
    revisado: "20 de octubre de 2026"
  },
  {
    // Su Linktree oficial (linktr.ee/servirperu, enlaza a gob.pe) lo pone. Página del canal: «Cursos y talleres gratuitos sobre gestión pública», 1 700 seguidores.
    id: "servir-enap-canal",
    nombre: "Cursos gratis de gesti\xF3n p\xFAblica (SERVIR)",
    url: "https://whatsapp.com/channel/0029Vb7y9lf5Ui2alFCGYq3e",
    fuente: "https://linktr.ee/servirperu",
    administra: "SERVIR (Escuela Nacional de Administraci\xF3n P\xFAblica)",
    tema: "Cursos gratis",
    detalle: "Canal de la Escuela Nacional de Administraci\xF3n P\xFAblica de SERVIR: cursos y talleres gratuitos sobre gesti\xF3n p\xFAblica.",
    revisado: "20 de octubre de 2026"
  },
  {
    // Su Linktree oficial (linktr.ee/concytecperu) lo pone. Página del canal: «CONCYTEC», 1 800 seguidores.
    id: "concytec-canal",
    nombre: "Concytec (canal oficial)",
    url: "https://whatsapp.com/channel/0029Vb7ay0jG3R3iRgrJ6e42",
    fuente: "https://linktr.ee/concytecperu",
    administra: "el Concytec",
    tema: "Investigaci\xF3n",
    detalle: "Canal oficial del Consejo Nacional de Ciencia y Tecnolog\xEDa: concursos, fondos y becas de investigaci\xF3n, y noticias de ciencia.",
    revisado: "20 de octubre de 2026"
  }
];

// src/data/canalesUniversidadesPe.ts
var REVISADO = "10 de octubre de 2026";
var UNA_CUENTA = "la cuenta \xABEstudiante Universitario del Per\xFA\xBB (no es oficial)";
var DOS_CUENTAS = "las cuentas \xABEstudiante Universitario del Per\xFA\xBB y \xABUniversitario\xBB (no es oficial)";
var FILAS = [
  // ---------- Universidades públicas
  ["unac", "unac", "UNAC | Universidad Nacional del Callao", "22 000", 207, true],
  ["untels", "untels", "UNTELS | Universidad Nacional Tecnol\xF3gica de Lima Sur", "5 800", 48, true],
  ["undc", "undc", "UNDC | Universidad Nacional de Ca\xF1ete", "7 600", 174],
  ["unab", "unab", "UNAB | Universidad Nacional de Barranca", "12 300", 250],
  ["unjfsc", "unjfsc", "UNJFSC | Universidad Nacional Jos\xE9 Faustino S\xE1nchez Carri\xF3n", "39 900", 452, true],
  ["unt", "unt", "UNT | Universidad Nacional de Trujillo", "24 500", 163, true],
  ["unf", "unf", "UNF | Universidad Nacional de Frontera", "14 300", 34],
  ["unprg", "unprg", "UNPRG | Universidad Nacional Pedro Ruiz Gallo", "42 400", 247, true],
  ["uns", "uns", "UNS | Universidad Nacional del Santa", "18 300", 265],
  ["unc", "unc", "UNC | Universidad Nacional de Cajamarca", "8 300", 137, true],
  ["unach", "unach", "UNACH | Universidad Nacional Aut\xF3noma de Chota", "10 200", 108],
  ["unj", "unj", "UNJ | Universidad Nacional de Ja\xE9n", "8 900", 79],
  ["untrm", "untrm", "UNTRM | Universidad Nacional Toribio Rodr\xEDguez de Mendoza de Amazonas", "15 400", 399],
  ["uncp", "uncp", "UNCP | Universidad Nacional del Centro del Per\xFA", "7 900", 135, true],
  ["unaat", "unaat", "UNAAT | Universidad Nacional Aut\xF3noma Altoandina de Tarma", "12 400", 201],
  ["uniscjsa", "uniscjsa", "UNISCJSA | Universidad Nacional Intercultural de la Selva Central Juan Santos Atahualpa", "9 400", 33],
  ["unheval", "unheval", "UNHEVAL | Universidad Nacional Hermilio Valdiz\xE1n", "24 200", 168],
  ["unas", "unas", "UNAS | Universidad Nacional Agraria de la Selva", "19 300", 237, true],
  ["undac", "undac", "UNDAC | Universidad Nacional Daniel Alcides Carri\xF3n", "16 500", 196, true],
  ["unh", "unh", "UNH | Universidad Nacional de Huancavelica", "15 400", 459],
  ["unat", "unat", "UNAT | Universidad Nacional Aut\xF3noma de Tayacaja Daniel Hern\xE1ndez Morillo", "4 700", 69],
  ["unsch", "unsch", "UNSCH | Universidad Nacional de San Crist\xF3bal de Huamanga", "36 900", 2808, true],
  ["unah", "unah", "UNAH | Universidad Nacional Aut\xF3noma de Huanta", "6 500", 80],
  ["unsa", "unsa", "UNSA | Universidad Nacional de San Agust\xEDn de Arequipa", "8 500", 109],
  ["unsaac", "unsaac", "UNSAAC | Universidad Nacional de San Antonio Abad del Cusco", "94 600", 1366, true],
  ["uniq", "uniq", "UNIQ | Universidad Nacional Intercultural de Quillabamba", "8 000", 129, true],
  ["unap", "unap-loreto", "UNAP | Universidad Nacional de la Amazon\xEDa Peruana", "19 400", 333, true],
  // Iquitos
  ["unaj", "unaj", "UNAJ | Universidad Nacional de Juliaca", "8 000", 165],
  ["unajma", "unajma", "UNAJMA | Universidad Nacional Jos\xE9 Mar\xEDa Arguedas", "14 100", 114],
  ["unjbg", "unjbg", "UNJBG | Universidad Nacional Jorge Basadre Grohmann", "16 300", 411],
  ["unaaa", "unaaa", "UNAAA | Universidad Nacional Aut\xF3noma de Alto Amazonas", "6 500", 49],
  ["unu", "unu", "UNU | Universidad Nacional de Ucayali", "17 000", 100, true],
  ["una", "unap-puno", "UNA | Universidad Nacional del Altiplano de Puno", "15 500", 489, true],
  // Puno
  // ---------- Universidades privadas
  ["utp", "utp", "UTP | Universidad Tecnol\xF3gica del Per\xFA", "44 400", 941],
  ["ucv", "ucv", "UCV | Universidad C\xE9sar Vallejo", "27 300", 360],
  ["upn", "upn", "UPN | Universidad Privada del Norte", "84 500", 1676],
  ["upc", "upc", "UPC | Universidad Peruana de Ciencias Aplicadas", "48 400", 1915],
  ["usmp", "usmp", "USMP | Universidad de San Mart\xEDn de Porres", "18 700", 254],
  ["pucp", "pucp", "PUCP | Pontificia Universidad Cat\xF3lica del Per\xFA", "34 000", 377, true],
  ["upeu", "upeu", "UPeU | Universidad Peruana Uni\xF3n", "26 100", 615],
  ["ucss", "ucss", "UCSS | Universidad Cat\xF3lica Sedes Sapientiae", "20 200", 77],
  ["usil", "usil", "USIL | Universidad San Ignacio de Loyola", "7 200", 102, true],
  ["upsjb", "upsjb", "UPSJB | Universidad Privada San Juan Bautista", "4 600", 109],
  ["utec", "utec", "UTEC | Universidad de Ingenier\xEDa y Tecnolog\xEDa", "9 800", 125],
  ["urp", "urp", "URP | Universidad Ricardo Palma", "1 700", 35],
  ["uesan", "uesan", "UESAN | Universidad ESAN", "3 900", 41],
  ["upch", "upch", "UPCH | Universidad Peruana Cayetano Heredia", "9 800", 194],
  ["unife", "unife", "UNIF\xC9 | Universidad Femenina del Sagrado Coraz\xF3n", "8 100", 70, true],
  ["udep", "udep", "UDEP | Universidad de Piura", "16 100", 199],
  ["upao", "upao", "UPAO | Universidad Privada Antenor Orrego", "22 900", 218],
  ["ucsm", "ucsm", "UCSM | Universidad Cat\xF3lica Santa Mar\xEDa", "25 600", 108, true],
  ["uch", "uch", "UCH | Universidad de Ciencias y Humanidades", "7 700", 41],
  ["usat", "usat", "USAT | Universidad Cat\xF3lica Santo Toribio de Mogrovejo", "5 400", 41],
  ["uss", "uss", "USS | Universidad Se\xF1or de Sip\xE1n", "14 100", 143],
  ["upla", "upla", "UPLA | Universidad Peruana Los Andes", "11 800", 220],
  ["udh", "udh", "UDH | Universidad de Hu\xE1nuco", "24 200", 231],
  ["upt", "upt", "UPT | Universidad Privada de Tacna", "6 800", 46],
  ["uai", "uai", "UAI | Universidad Aut\xF3noma de Ica", "17 200", 76]
];
var detalleDe = (nombre, miembros, publicaciones) => `Grupo p\xFAblico de Facebook de la comunidad de la ${nombre.split(" | ")[0]} (unos ${miembros} miembros, ${publicaciones} publicaciones el \xFAltimo mes). No es oficial.`;
var DE_SIGLA_PE = FILAS.map(([slug, universityId, nombre, miembros, publicaciones, dosCuentas]) => ({
  id: `${slug}-pe-fb`,
  universityId,
  nombre,
  plataforma: "facebook",
  url: `https://www.facebook.com/groups/${slug}.pe`,
  origen: "abierta",
  detalle: detalleDe(nombre, miembros, publicaciones),
  administra: dosCuentas ? DOS_CUENTAS : UNA_CUENTA,
  revisado: REVISADO
}));
var UNA_PERSONA = "una persona (no es oficial)";
var SIN_DATO = "no se vio qui\xE9n lo administra (no es oficial)";
var FILAS_OTRAS = [
  ["untumbes-fb", "untumbes", "UNTUMBES | Universidad Nacional de Tumbes", "untumbes", "13 500", 122, DOS_CUENTAS],
  ["unsm-fb", "unsm", "UNSM | Universidad Nacional de San Mart\xEDn de Tarapoto", "641967688202335", "7 100", 124, UNA_PERSONA],
  ["unica-fb", "unica", "UNICA | Universidad Nacional San Luis Gonzaga de Ica", "1547904782737781", "5 100", 257, UNA_PERSONA],
  ["unamba-fb", "unamba", "UNAMBA | Universidad Nacional Micaela Bastidas de Apur\xEDmac", "1161692521709739", "4 200", 52, UNA_PERSONA],
  ["uac-pe-fb", "uac", "UAC | Universidad Andina del Cusco", "uandinadelcusco.pe", "28 700", 450, UNA_CUENTA],
  ["ucsp-fb", "ucsp", "UCSP | Universidad Cat\xF3lica San Pablo de Arequipa", "ucsp.peru", "18 900", 73, UNA_CUENTA],
  ["ucsur-fb", "ucsur", "UCSUR | Universidad Cient\xEDfica del Sur", "ucientificasur.pe", "56 700", 3600, UNA_CUENTA],
  ["up-fb", "up", "UP | Universidad del Pac\xEDfico", "universidaddelpacfico.pe", "7 900", 41, UNA_CUENTA],
  ["uc-fb", "uc", "UC | Universidad Continental", "856034244471064", "100 700", 3384, SIN_DATO],
  ["autonoma-fb", "autonoma", "UA | Universidad Aut\xF3noma del Per\xFA", "uautonoma.pe", "21 000", 281, UNA_CUENTA],
  // `unp.pe` lo ocupa otro grupo (privado, 1 miembro); el de la red es `unp.edu.pe`.
  ["unp-fb", "unp", "UNP | Universidad Nacional de Piura", "unp.edu.pe", "27 300", 220, UNA_CUENTA]
];
var OTRAS = FILAS_OTRAS.map(([id, universityId, nombre, direccion, miembros, publicaciones, administra]) => ({
  id,
  universityId,
  nombre,
  plataforma: "facebook",
  url: `https://www.facebook.com/groups/${direccion}`,
  origen: "abierta",
  detalle: detalleDe(nombre, miembros, publicaciones),
  administra,
  revisado: REVISADO
}));
var CANALES_UNIVERSIDADES_PE = [...DE_SIGLA_PE, ...OTRAS];

// src/data/canalesUniversidades.ts
function tipoDeCanal(url, plataforma) {
  if (plataforma === "facebook") return "grupo";
  if (plataforma === "whatsapp") return /whatsapp\.com\/channel\//i.test(url) ? "canal" : "grupo";
  return /t\.me\/(\+|joinchat\/)/i.test(url) ? "grupo" : "canal";
}
var FECHA_REVISION_CANALES = "8 de octubre de 2026";
var CANALES_MANUALES = [
  {
    id: "unsa-admision",
    universityId: "unsa",
    nombre: "Admisi\xF3n UNSA",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029Vakqevy65yD9RImiGX0O",
    origen: "universidad",
    detalle: "Canal oficial de la Direcci\xF3n de Admisi\xF3n (para postulantes)"
  },
  {
    id: "unsaac-comedor",
    universityId: "unsaac",
    nombre: "Comedor Universitario UNSAAC",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029VaAdNumKAwEoOEGRVx2o",
    origen: "universidad",
    detalle: "Se presenta como el canal del comedor universitario de la UNSAAC"
  },
  {
    id: "unt-registros",
    universityId: "unt",
    nombre: "Registros Acad\xE9micos UNT",
    plataforma: "telegram",
    url: "https://t.me/urauntoficial",
    origen: "universidad",
    detalle: "Unidad de Registros Acad\xE9micos: constancias y matr\xEDcula"
  },
  {
    // Su sitio oficial de admisión (admision.unsm.edu.pe) enlaza este canal. Página del canal: «Canal oficial de la Dirección de Admisión de la Universidad Nacional de San Martín», 1 500 seguidores.
    id: "unsm-admision",
    universityId: "unsm",
    nombre: "Admisi\xF3n UNSM Oficial",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029VbCbzaeDjiOaRU9CDi2E",
    origen: "universidad",
    detalle: "Canal oficial de la Direcci\xF3n de Admisi\xF3n (para postulantes): informaci\xF3n sobre los ex\xE1menes ordinario y extraordinario",
    revisado: "10 de octubre de 2026"
  },
  {
    // La nota «Implementación de canal de WhatsApp Bolsa de Trabajo - UNMSM» de sistemas.unmsm.edu.pe (Oficina de Servicio Social) traía este enlace;
    // el 20/10/2026 la nota ya daba 404, pero el buscador la conservaba con el enlace. Página del canal: «Bolsa de Trabajo - UNMSM», 14 mil seguidores.
    id: "unmsm-bolsa-trabajo",
    universityId: "unmsm",
    nombre: "Bolsa de Trabajo UNMSM (canal)",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029VaYkR1bGOj9h6osZYA1I",
    origen: "universidad",
    detalle: "Canal de la Unidad de Bolsa y Empleo de la Oficina de Servicio Social de San Marcos: ofertas de empleo y pr\xE1cticas para estudiantes y egresados.",
    administra: "la Bolsa de Trabajo de la UNMSM",
    revisado: "20 de octubre de 2026"
  },
  {
    // El sitio del Centro Preuniversitario de la UNI (cepre.uni.edu.pe) lo anuncia como su canal oficial; 14 000 seguidores.
    id: "uni-cepre",
    universityId: "uni",
    nombre: "CEPREUNI (canal oficial)",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029VahG0E8DOQIUvGrYII0S",
    origen: "universidad",
    detalle: "Canal oficial del Centro Preuniversitario de la UNI: avisos para la comunidad CEPREUNI",
    revisado: "10 de octubre de 2026"
  },
  {
    // La nota «Unasam lanza su canal de WhatsApp» de su ficha oficial en gob.pe (gob.pe/institucion/unasam/noticias/836814) trae este enlace. Página del canal: «RTV Unasam», 674 seguidores.
    id: "unasam-rtv",
    universityId: "unasam",
    nombre: "RTV Unasam (canal oficial)",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029Va3Z46ZI7BeHaRQ3M20g",
    origen: "universidad",
    detalle: "Informaci\xF3n actualizada de \xFAltimo momento de la Universidad Nacional Santiago Ant\xFAnez de Mayolo, seg\xFAn su propia nota oficial",
    revisado: "10 de octubre de 2026"
  },
  {
    // Su página oficial de Facebook (UNIoficial.pe) invita a la comunidad universitaria a unirse a este canal (reels de oct. 2023). Página del canal: «Universidad Nacional de Ingeniería (UNI)», 45 000 seguidores: «Canal oficial de la UNI».
    id: "uni-oficial-canal",
    universityId: "uni",
    nombre: "UNI (canal oficial)",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029Va2fskBIN9ig90vuHk1f",
    origen: "universidad",
    detalle: "Canal oficial de la Universidad Nacional de Ingenier\xEDa (45 000 seguidores): avisos y novedades para su comunidad",
    revisado: "10 de octubre de 2026"
  },
  {
    // Lo lista el directorio findchannels.com. Página del canal: «Universidad Nacional Tecnológica de Lima Sur — ¡Bienvenidos al Canal Untels! … nuestra casa superior de estudios», 2 400 seguidores. El sitio de la UNTELS no lo enlaza (se revisaron su inicio, /admision, /contacto y su ficha de gob.pe).
    id: "untels-canal",
    universityId: "untels",
    nombre: "Canal UNTELS",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029VaXO3mwE50UZdmsQSO3O",
    origen: "abierta",
    detalle: "Canal de WhatsApp que se presenta como el de la UNTELS (2 400 seguidores). Su web no lo enlaza, as\xED que no es oficial confirmado.",
    administra: "se presenta como la propia universidad (sin confirmar)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Lo lista el directorio findchannels.com. Página del canal: «Developer Student Clubs UTP - Events», 574 seguidores.
    id: "utp-dsc",
    universityId: "utp",
    nombre: "Developer Student Clubs UTP (eventos)",
    plataforma: "whatsapp",
    url: "https://whatsapp.com/channel/0029Vad7xnsL7UVQbpJKSC3W",
    origen: "estudiantil",
    detalle: "Canal de WhatsApp del club Developer Student Clubs de la UTP (574 seguidores): eventos, talleres y hackatones de tecnolog\xEDa. Es un club estudiantil, no oficial de la universidad.",
    administra: "el club estudiantil (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    id: "unmsm-rtv",
    universityId: "unmsm",
    nombre: "RTV San Marcos",
    plataforma: "telegram",
    url: "https://t.me/RTV_SM",
    origen: "universidad",
    detalle: "Se presenta como el canal oficial de la Decana de Am\xE9rica"
  },
  {
    id: "uni-figmm",
    universityId: "uni",
    nombre: "Estudiantes y amigos de la FIGMM-UNI",
    plataforma: "telegram",
    url: "https://t.me/joinchat/RS53TBTd7GtJSyqR6bS3tg",
    origen: "estudiantil",
    detalle: "Grupo de estudiantes de Ing. Geol\xF3gica, Minera y Metal\xFArgica (no oficial)"
  },
  {
    // Público, creado el 6/5/2014, 8 355 miembros; 107 publicaciones el último mes. La página no dice quién lo administra ni da una descripción.
    id: "unmsm-educacion-fb",
    universityId: "unmsm",
    nombre: "Facultad de Educaci\xF3n - UNMSM - Innovaci\xF3n Educativa",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/268041783378137",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook con el nombre de la Facultad de Educaci\xF3n de la UNMSM (m\xE1s de 8 000 miembros). No es oficial y no se pudo confirmar qui\xE9n lo administra.",
    administra: "sus propios creadores (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 27/10/2021, 12 893 miembros; 60 publicaciones el último mes. Lo administran las cuentas «Estudiante Universitario del Perú» y «Universitario». Reglas: sin publicidad ni proselitismo político.
    id: "une-fb",
    universityId: "une",
    nombre: "UNE | Universidad Nacional de Educaci\xF3n Enrique Guzm\xE1n y Valle",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/une.pe",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos y profesionales de la UNE (m\xE1s de 12 000 miembros). No es oficial: sus reglas proh\xEDben la publicidad y el proselitismo pol\xEDtico.",
    administra: "la cuenta \xABEstudiante Universitario del Per\xFA\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 12/10/2021, 9 302 miembros; 56 publicaciones el último mes. Misma administradora y mismas reglas que el de la UNE.
    id: "unamad-pe-fb",
    universityId: "unamad",
    nombre: "UNAMAD | Universidad Nacional Amaz\xF3nica de Madre de Dios",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/unamad.pe",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos y profesionales de la UNAMAD (m\xE1s de 9 000 miembros). No es oficial: sus reglas proh\xEDben la publicidad y el proselitismo pol\xEDtico.",
    administra: "la cuenta \xABEstudiante Universitario del Per\xFA\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 1/5/2018 (Puerto Maldonado), 9 265 miembros; 34 publicaciones el último mes. Lo administra una persona; su página solo trae la visión de la universidad.
    id: "unamad-fb",
    universityId: "unamad",
    nombre: "UNAMAD (Puerto Maldonado)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/UNAMAD",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la comunidad de la UNAMAD en Puerto Maldonado (m\xE1s de 9 000 miembros, creado en 2018). No es oficial.",
    administra: "una persona (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 7/3/2025, 1 723 miembros; 53 publicaciones el último mes. Lo administra una persona.
    id: "unamad-admision-fb",
    universityId: "unamad",
    nombre: "UNAMAD Admisi\xF3n 2026",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/1111544224102827",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook para postulantes y estudiantes de la UNAMAD (m\xE1s de 1 700 miembros): admisi\xF3n, noticias y resultados. No es oficial.",
    administra: "una persona (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 17/12/2009, 9 098 miembros; 65 publicaciones el último mes. «Alumnos, Egresados y Profesores de la Facultad…» según su descripción.
    id: "unmsm-derecho-fb",
    universityId: "unmsm",
    nombre: "Facultad de Derecho y Ciencia Pol\xEDtica de la UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/213253217995",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos, egresados y profesores de la Facultad de Derecho y Ciencia Pol\xEDtica de la UNMSM (m\xE1s de 9 000 miembros, desde 2009). No es oficial.",
    administra: "sus propios creadores (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 25/6/2013, 12 939 miembros; 250 publicaciones el último mes. Facebook lo muestra como «Grupo de Instituto de Estudios Jurídicos y Empresariales».
    id: "unmsm-estudiantes-derecho-fb",
    universityId: "unmsm",
    nombre: "Estudiantes de Derecho UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/317624861705333",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Derecho de la UNMSM (casi 13 000 miembros, desde 2013). Facebook lo muestra ligado al Instituto de Estudios Jur\xEDdicos y Empresariales. No es oficial.",
    administra: "la p\xE1gina \xABInstituto de Estudios Jur\xEDdicos y Empresariales\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 20/5/2021 (Arequipa), 4 614 miembros; 34 publicaciones el último mes. Lo administran las cuentas «Derecho UNSA Arequipa» y «Derecho».
    id: "unsa-derecho-fb",
    universityId: "unsa",
    nombre: "Facultad de Derecho UNSA",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/derechounsa23",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Derecho de la UNSA, en Arequipa (m\xE1s de 4 000 miembros, desde 2021). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "las cuentas \xABDerecho UNSA Arequipa\xBB y \xABDerecho\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 20/10/2011, 5 163 miembros; 97 publicaciones el último mes. «Grupo de la carrera de Trabajo Social de la Facultad de Filosofía y Letras, exclusivamente para los estudiantes…». No se pudieron ver sus publicaciones.
    id: "unt-trabajo-social-fb",
    universityId: "unt",
    nombre: "Trabajo Social UNT",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/189507177790206",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la carrera de Trabajo Social de la UNT, Facultad de Filosof\xEDa y Letras (m\xE1s de 5 000 miembros, desde 2011). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 16/3/2014, 2 448 miembros; 250 publicaciones el último mes. Sin descripción. No se pudieron ver sus publicaciones.
    id: "uncp-trabajo-social-fb",
    universityId: "uncp",
    nombre: "Trabajo Social UNCP",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/1431362553772050",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de Trabajo Social de la UNCP (unos 2 400 miembros, 250 publicaciones al mes, desde 2014). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 29/1/2018, 3 864 miembros; 56 publicaciones el último mes. Su descripción dice que es el espacio abierto de difusión de la Facultad (no se confirmó). No se pudieron ver sus publicaciones.
    id: "unsa-enfermeria-fb",
    universityId: "unsa",
    nombre: "Facultad de Enfermer\xEDa UNSA",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/1585695144848036",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Enfermer\xEDa de la UNSA (casi 4 000 miembros, desde 2018). Se presenta como espacio de difusi\xF3n de la facultad. No es oficial: no se confirm\xF3.",
    administra: "dice ser de la facultad (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 25/4/2023, 2 448 miembros; 56 publicaciones el último mes. «Miembros de la Facultad de Medicina Humana de la UNMSM». No se pudieron ver sus publicaciones.
    id: "unmsm-medicina-fb",
    universityId: "unmsm",
    nombre: "Facultad de Medicina San Fernando UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/facultaddemedicinaunmsm",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de miembros de la Facultad de Medicina Humana de la UNMSM (m\xE1s de 2 400 miembros, desde 2023). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/4/2012, 6 784 miembros; 378 publicaciones el último mes. Para alumnos y ex alumnos de Medicina Humana. No se pudieron ver sus publicaciones.
    id: "ucv-medicina-fb",
    universityId: "ucv",
    nombre: "UCV - Medicina Humana",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/UCV.MedicinaHumana.Peru",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos y ex alumnos de Medicina Humana de la UCV (casi 7 000 miembros, 378 publicaciones al mes, desde 2012). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 26/4/2011, 1 805 miembros; 44 publicaciones el último mes. Su descripción dice «Grupo Oficial en Facebook de la Facultad» (no se confirmó). No se pudieron ver sus publicaciones.
    id: "unjfsc-medicina-fb",
    universityId: "unjfsc",
    nombre: "Medicina UNJFSC (Huacho)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/medicina.unjfsc",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Medicina Humana de la UNJFSC, Huacho (m\xE1s de 1 800 miembros, desde 2011). Dice ser el oficial de la facultad; no es oficial confirmado.",
    administra: "dice ser de la facultad (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 16/10/2016, 9 019 miembros; 43 publicaciones el último mes. «Grupo abierto… conformado por alumnos y ex alumnos» de la PUCP. No se pudieron ver sus publicaciones.
    id: "pucp-economia-fb",
    universityId: "pucp",
    nombre: "Econom\xEDa PUCP",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/683233705164970",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos y ex alumnos de Econom\xEDa de la PUCP (m\xE1s de 9 000 miembros, 43 publicaciones al mes, desde 2016). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 19/6/2009, 15 193 miembros; 339 publicaciones el último mes. «Alma Mater Virtual de la Facultad de Arquitectura de la UPC». No se pudieron ver sus publicaciones.
    id: "upc-arquitectura-fb",
    universityId: "upc",
    nombre: "Facultad de Arquitectura UPC (Lima)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/fa.upc",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Arquitectura de la UPC en Lima (m\xE1s de 15 000 miembros, 339 publicaciones al mes, desde 2009). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 1/1/2023, 1 011 miembros; 78 publicaciones el último mes. «Facultad de Odontología de la UNMSM». No se pudieron ver sus publicaciones.
    id: "unmsm-odontologia-fb",
    universityId: "unmsm",
    nombre: "Facultad de Odontolog\xEDa UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/odontologiaunmsm",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Odontolog\xEDa de la UNMSM (m\xE1s de 1 000 miembros, 78 publicaciones al mes, desde 2023). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Perú), creado el 8/3/2011, 3 770 miembros; 245 publicaciones el último mes. «Estudiantes y egresados de la facultad de odontología USMP». No se pudieron ver sus publicaciones.
    id: "usmp-odontologia-fb",
    universityId: "usmp",
    nombre: "USMP Odontolog\xEDa",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/189027484465614",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes y egresados de Odontolog\xEDa de la USMP (casi 3 800 miembros, 245 publicaciones al mes, desde 2011). No es oficial: no se vio qui\xE9n lo administra.",
    administra: "no se vio qui\xE9n lo administra (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 1/1/2023, 1 719 miembros; 82 publicaciones el último mes. Se presenta como «Portal de la Facultad de Odontología UPCH» (no se confirmó). No se pudieron ver sus publicaciones.
    id: "upch-estomatologia-fb",
    universityId: "upch",
    nombre: "Facultad de Estomatolog\xEDa UPCH",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/upchoficial",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Estomatolog\xEDa de la UPCH (m\xE1s de 1 700 miembros, 82 publicaciones al mes, desde 2023). Se presenta como portal de la facultad. No es oficial: no se confirm\xF3.",
    administra: "dice ser de la facultad (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 16/1/2022, 1 576 miembros; 139 publicaciones el último mes; administran «Jose» y una cuenta llamada «Facultad». Se presenta como grupo académico y científico de la facultad.
    id: "uncp-antropologia-fb",
    universityId: "uncp",
    nombre: "Facultad de Antropolog\xEDa UNCP",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/597281131334476",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Antropolog\xEDa de la UNCP, en Huancayo (unos 1 600 miembros, 139 publicaciones al mes, desde 2022). No es oficial: se presenta como grupo de la facultad, pero no se confirm\xF3.",
    administra: "dice ser de la facultad (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/10/2012 (nombre cambiado el 10/7/2019), 3 063 miembros; 46 publicaciones el último mes.
    id: "unsaac-arqueologia-fb",
    universityId: "unsaac",
    nombre: "E.P. Arqueolog\xEDa - UNSAAC",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/295359323905838",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Escuela Profesional de Arqueolog\xEDa de la UNSAAC, en Cusco (unos 3 100 miembros, 46 publicaciones al mes, desde 2012). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "una persona o la escuela (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 13/3/2025, 1 355 miembros; 144 publicaciones el último mes. No se pudo ver quién lo administra.
    id: "unac-grupo-fb",
    universityId: "unac",
    nombre: "UNAC | Universidad Nacional del Callao",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/677675844718134",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Universidad Nacional del Callao (unos 1 400 miembros, 144 publicaciones al mes, desde 2025). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "no se sabe (no es oficial)",
    revisado: "14 de octubre de 2026"
  },
  {
    // Público, creado el 12/3/2025, 5 442 miembros; 108 publicaciones el último mes. No se pudo ver quién lo administra.
    id: "une-la-cantuta-fb",
    universityId: "une",
    nombre: "La Cantuta | Universidad Nacional de Educaci\xF3n (UNE)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/455608610874670",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de La Cantuta, la Universidad Nacional de Educaci\xF3n Enrique Guzm\xE1n y Valle (unos 5 400 miembros, 108 publicaciones al mes, desde 2025). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "no se sabe (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 25/5/2025, 2 369 miembros; 146 publicaciones el último mes.
    id: "une-cantuta-estudiantes-fb",
    universityId: "une",
    nombre: "Universidad Nacional de Educaci\xF3n (UNE) - La Cantuta",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/1198186378279228",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la UNE - La Cantuta (unos 2 400 miembros, 146 publicaciones al mes, desde 2025). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "no se sabe (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 1/2/2010, 1 513 miembros; 57 publicaciones el último mes; administran «Historia» y «Toño». Profesores, egresados y estudiantes de la E.A.P. de Historia.
    id: "unmsm-historia-fb",
    universityId: "unmsm",
    nombre: "Historia - UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/275012785997",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de profesores, egresados y estudiantes de la Escuela de Historia de la UNMSM (unos 1 500 miembros, 57 publicaciones al mes, desde 2010). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "dos cuentas (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 10/6/2012, 2 611 miembros; 32 publicaciones el último mes; administra la cuenta «Cehunfv» y 3 más (parece el centro de estudiantes).
    id: "unfv-historia-fb",
    universityId: "unfv",
    nombre: "Historia - UNFV",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/142917329178027",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de la Escuela Profesional de Historia de la UNFV (unos 2 600 miembros, 32 publicaciones al mes, desde 2012). No es oficial: lo administra la cuenta \xABCehunfv\xBB y 3 m\xE1s, sin confirmar.",
    administra: "la cuenta \xABCehunfv\xBB y 3 m\xE1s (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 23/7/2008, 2 010 miembros; 43 publicaciones el último mes; su descripción dice que su alma mater es la PUCP. Un resultado de búsqueda mostró la oferta de libros.
    id: "pucp-historia-fb",
    universityId: "pucp",
    nombre: "Historiadores PUCP",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/32135946322",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de historiadores vinculados a la PUCP (unos 2 000 miembros, 43 publicaciones al mes, desde 2008). No es oficial: no se confirm\xF3 que lo lleve la universidad. Se ven ofertas de libros.",
    administra: "una persona y 3 m\xE1s (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 11/8/2015, 2 144 miembros; 34 publicaciones el último mes; 4 administradores. Se presenta como grupo creado por la carrera.
    id: "unsaac-obstetricia-fb",
    universityId: "unsaac",
    nombre: "Escuela Obstetricia UNSAAC (sede Andahuaylas)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/escuelaobstetricia",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Escuela Profesional de Obstetricia de la UNSAAC, sede Andahuaylas (unos 2 100 miembros, 34 publicaciones al mes, desde 2015). No es oficial: dice ser creado por la carrera, pero no se confirm\xF3.",
    administra: "dice ser de la carrera (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 12/6/2011 (Cusco), 3 284 miembros; 76 publicaciones el último mes; 2 administradores. Se presenta como el grupo de la escuela, sin confirmar.
    id: "unsaac-comunicacion-fb",
    universityId: "unsaac",
    nombre: "E.P. de Ciencias de la Comunicaci\xF3n - UNSAAC",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/ccunsaac",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Escuela Profesional de Ciencias de la Comunicaci\xF3n de la UNSAAC, en Cusco (unos 3 300 miembros, 76 publicaciones al mes, desde 2011). No es oficial: se presenta como grupo de la escuela, pero no se confirm\xF3.",
    administra: "dice ser de la escuela (sin confirmar, no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 4/11/2010 (Lima), 1 141 miembros; 38 publicaciones el último mes. Lo administra una persona; su descripción invita a una reunión de egresados. No se pudieron ver sus publicaciones (la página pide iniciar sesión).
    id: "unmsm-quimica-fb",
    universityId: "unmsm",
    nombre: "UNMSM - Qu\xEDmica - Ing. Qu\xEDmica",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/167281149956472",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes y egresados de Qu\xEDmica e Ingenier\xEDa Qu\xEDmica de la UNMSM (unos 1 100 miembros, 38 publicaciones al mes, desde 2010). No es oficial: lo administra una persona.",
    administra: "una persona (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/1/2009 (Santiago de Surco, Lima), 4 539 miembros; 54 publicaciones el último mes. Lo administra una persona. No se pudieron ver sus publicaciones (la página pide iniciar sesión).
    id: "urp-medicina-veterinaria-fb",
    universityId: "urp",
    nombre: "URP Medicina Veterinaria",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/URPmedicinaveterinaria",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Escuela de Medicina Veterinaria de la Universidad Ricardo Palma (m\xE1s de 4 500 miembros, desde 2009). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "una persona (no es oficial)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 18/1/2012, 4 269 miembros; 82 publicaciones el último mes. Lo administra una persona. (El otro grupo de la facultad, `1171576166269161`, es privado.)
    id: "unmsm-contables-fb",
    universityId: "unmsm",
    nombre: "Facultad de Ciencias Contables UNMSM",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/238586286216426",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Ciencias Contables de la UNMSM (m\xE1s de 4 000 miembros, desde 2012). No es oficial: no se confirm\xF3 qui\xE9n lo administra.",
    administra: "una persona (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 6/10/2011 (Arequipa), 6 813 miembros; 93 publicaciones el último mes. Lo administra una cuenta con el nombre de la facultad.
    id: "unsa-contables-fb",
    universityId: "unsa",
    nombre: "Facultad de Ciencias Contables y Financieras UNSA",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/259344630776936",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la Facultad de Ciencias Contables y Financieras de la UNSA, en Arequipa (casi 7 000 miembros, desde 2011). No es oficial: lo administra una cuenta con el nombre de la facultad, pero no se confirm\xF3 que sea de ella.",
    administra: "una cuenta con el nombre de la facultad (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 16/6/2011 (Lima), 108 850 miembros; 671 publicaciones el último mes. Administra la cuenta «Estudiantes de la UNI» y 2 más; Facebook lo muestra como «Grupo de La Facultad de Ing. Geológica, Minera y Metalúrgica -UNI-». Su regla 1 manda a t.me/UNIPeru, que no existe.
    id: "uni-grupo-fb",
    universityId: "uni",
    nombre: "Universidad Nacional de Ingenier\xEDa (UNI)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/GrupoUNIperu",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la comunidad de la UNI, con m\xE1s de 108 000 miembros y unas 670 publicaciones al mes. No es oficial: lo administra la cuenta \xABEstudiantes de la UNI\xBB.",
    administra: "la cuenta \xABEstudiantes de la UNI\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 31/10/2021, 4 939 miembros; 117 publicaciones el último mes. Misma cuenta «Estudiante Universitario del Perú» que los de la UNE y la UNAMAD.
    id: "uni-pe-fb",
    universityId: "uni",
    nombre: "UNI | Universidad Nacional de Ingenier\xEDa (alumnos y profesionales)",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/uni.pe",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de alumnos y profesionales de la UNI (casi 5 000 miembros, desde 2021). No es oficial: sus reglas son las mismas de los grupos \xAB.pe\xBB de otras universidades.",
    administra: "la cuenta \xABEstudiante Universitario del Per\xFA\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 31/10/2021, 16 564 miembros; 235 publicaciones el último mes. Misma cuenta «Estudiante Universitario del Perú» y mismas reglas que los de la UNE, la UNAMAD y la UNI.
    id: "unalm-pe-fb",
    universityId: "unalm",
    nombre: "UNALM | Universidad Nacional Agraria La Molina",
    plataforma: "facebook",
    url: "https://www.facebook.com/groups/unalm.pe",
    origen: "abierta",
    detalle: "Grupo p\xFAblico de Facebook de la comunidad de la UNALM (m\xE1s de 16 000 miembros, unas 235 publicaciones al mes). No es oficial: sus reglas proh\xEDben la publicidad y el proselitismo pol\xEDtico.",
    administra: "la cuenta \xABEstudiante Universitario del Per\xFA\xBB (no es oficial)",
    revisado: "10 de octubre de 2026"
  }
];
var CANALES_UNIVERSIDADES = [...CANALES_MANUALES, ...CANALES_UNIVERSIDADES_PE];

// src/data/comunidadesPorCarrera.ts
var AREAS_COMUNIDADES = [
  { id: "programacion", etiqueta: "Programaci\xF3n" },
  { id: "educacion", etiqueta: "Educaci\xF3n" },
  { id: "derecho", etiqueta: "Derecho" },
  { id: "contabilidad", etiqueta: "Contabilidad" },
  { id: "administracion", etiqueta: "Administraci\xF3n" },
  { id: "veterinaria", etiqueta: "Veterinaria" },
  { id: "trabajosocial", etiqueta: "Trabajo Social" },
  { id: "marketing", etiqueta: "Marketing" },
  { id: "psicologia", etiqueta: "Psicolog\xEDa" },
  { id: "enfermeria", etiqueta: "Enfermer\xEDa" },
  { id: "medicina", etiqueta: "Medicina" },
  { id: "negociosint", etiqueta: "Negocios Internacionales" },
  { id: "economia", etiqueta: "Econom\xEDa" },
  { id: "arquitectura", etiqueta: "Arquitectura" },
  { id: "odontologia", etiqueta: "Odontolog\xEDa" },
  { id: "nutricion", etiqueta: "Nutrici\xF3n" },
  { id: "sociologia", etiqueta: "Sociolog\xEDa" },
  { id: "ciencias", etiqueta: "Ciencias B\xE1sicas" },
  { id: "turismo", etiqueta: "Turismo" },
  { id: "comunicacion", etiqueta: "Comunicaci\xF3n" },
  { id: "antropologia", etiqueta: "Antropolog\xEDa y Arqueolog\xEDa" },
  { id: "gastronomia", etiqueta: "Gastronom\xEDa" },
  { id: "farmacia", etiqueta: "Farmacia y Bioqu\xEDmica" },
  { id: "obstetricia", etiqueta: "Obstetricia" },
  { id: "historia", etiqueta: "Historia" },
  { id: "ingenieria", etiqueta: "Ingenier\xEDa" },
  { id: "ambiental", etiqueta: "Ambiental y Agronom\xEDa" }
];
var FECHA_REVISION_COMUNIDADES = "8 de octubre de 2026";
var COMUNIDADES_POR_CARRERA = [
  // ---------- Programación (en español, de habla hispana en general)
  {
    id: "mouredev",
    nombre: "MoureDev",
    area: "programacion",
    plataforma: "discord",
    tipo: "servidor",
    url: "https://discord.gg/mouredev",
    tema: "Programaci\xF3n general",
    detalle: "Comunidad de programaci\xF3n y desarrollo de software en espa\xF1ol: aprende a programar y mejora tus habilidades."
  },
  {
    id: "midudev",
    nombre: "midudev",
    area: "programacion",
    plataforma: "discord",
    tipo: "servidor",
    url: "https://discord.gg/midudev",
    tema: "JavaScript y web",
    detalle: "Comunidad de desarrollo web y programaci\xF3n en espa\xF1ol: JavaScript, React, Node.js, HTML, CSS y m\xE1s."
  },
  {
    id: "devtalles",
    nombre: "DevTalles",
    area: "programacion",
    plataforma: "discord",
    tipo: "servidor",
    url: "https://discord.com/invite/devtalles-1130900724499365958",
    tema: "Programaci\xF3n general",
    detalle: "Comunidad de desarrolladores de la academia DevTalles: apoyo a sus cursos y dudas de quienes quieren aprender programaci\xF3n."
  },
  {
    id: "python-en-espanol-discord",
    nombre: "Python en Espa\xF1ol",
    area: "programacion",
    plataforma: "discord",
    tipo: "servidor",
    url: "https://discord.gg/hablemospython",
    tema: "Python",
    detalle: "Servidor oficial de la comunidad hispanohablante de Python."
  },
  {
    id: "python-en-espanol",
    nombre: "Python en espa\xF1ol",
    area: "programacion",
    plataforma: "telegram",
    tipo: "grupo",
    url: "https://t.me/PythonEsp",
    tema: "Python",
    detalle: "Grupo de discusi\xF3n sobre el lenguaje Python en espa\xF1ol."
  },
  {
    id: "vuejs-es",
    nombre: "Hablemos de Vue.js",
    area: "programacion",
    plataforma: "telegram",
    tipo: "grupo",
    url: "https://t.me/vuejsEs",
    tema: "Vue.js",
    detalle: "Comunidad hispanohablante de Vue.js para compartir conocimientos, experiencias y c\xF3digo."
  },
  {
    id: "flutter-dart-es",
    nombre: "Flutter & Dart en Espa\xF1ol",
    area: "programacion",
    plataforma: "telegram",
    tipo: "grupo",
    url: "https://t.me/flutter_dart_spanish",
    tema: "Apps m\xF3viles (Flutter)",
    detalle: "Comunidad en espa\xF1ol sobre el SDK Flutter y el lenguaje Dart."
  },
  {
    id: "desarrolloweb",
    nombre: "Desarrollo web",
    area: "programacion",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/desarrolloweb",
    tema: "Desarrollo web",
    detalle: "Canal sobre dise\xF1o y desarrollo de aplicaciones web e informaci\xF3n de inter\xE9s general (solo avisos)."
  },
  // ---------- Programación peruana en Facebook (10/10/2026): se abrió la página pública de cada grupo (sin iniciar sesión) y se leyó «Información» y su actividad.
  {
    // Público, creado el 10/3/2015, 21 864 miembros (etiqueta «Perú»); 272 publicaciones el último mes. La publicación más reciente a la vista era un aviso de servicios.
    id: "fb-programadores-peru",
    nombre: "Programadores-Per\xFA",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1025454714150122",
    tema: "Programaci\xF3n general",
    detalle: "Grupo p\xFAblico de Facebook de programadores del Per\xFA (m\xE1s de 21 000 miembros). Algunos miembros publican avisos de sus servicios.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 29/11/2012, 17 115 miembros; 289 publicaciones el último mes (10 el día de la revisión). Sin administradores visibles.
    id: "fb-sistemas-informatica-peru",
    nombre: "Ingenier\xEDa de Sistemas, Inform\xE1tica y Computaci\xF3n (Per\xFA)",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/436054356456493",
    tema: "Sistemas e Inform\xE1tica",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes, egresados e ingenieros de Sistemas, Inform\xE1tica y Computaci\xF3n del Per\xFA (m\xE1s de 17 000 miembros).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 22/10/2015 (Lima), 14 725 miembros; solo 15 publicaciones el último mes. Tiene un reglamento largo (sin insultos, sin ofertas en captura, sin off-topic entre semana).
    id: "fb-programadores-en-peru",
    nombre: "Programadores en Per\xFA",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/Programadores.peru",
    tema: "Programaci\xF3n general",
    detalle: "Grupo p\xFAblico de Facebook de programadores de Lima y el Per\xFA (casi 15 000 miembros). Tiene reglamento estricto y publica poco: unas 15 publicaciones al mes.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 19/3/2013 (Lima), 9 619 miembros; 16 publicaciones el último mes. 6 administradores y 3 moderadores; código de conducta (Contributor Covenant). pythonperu.org no abre desde aquí: no se pudo confirmar desde su web.
    id: "fb-python-peru",
    nombre: "Python Per\xFA",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/pythonperu.org",
    tema: "Python",
    detalle: "Grupo p\xFAblico de Facebook sobre Python, de Lima (m\xE1s de 9 000 miembros), con c\xF3digo de conducta. No se pudo confirmar desde su web; publica poco (unas 16 al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 18/4/2012 (etiqueta «Perú»), 8 774 miembros; 65 publicaciones el último mes. La publicación más reciente a la vista era una convocatoria laboral.
    id: "fb-programadores-desarrolladores-peruanos",
    nombre: "Programadores y Desarrolladores Peruanos",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/274197409338267",
    tema: "Programaci\xF3n general",
    detalle: "Grupo p\xFAblico de Facebook de programadores y desarrolladores peruanos (m\xE1s de 8 000 miembros, desde 2012). Tambi\xE9n se publican convocatorias laborales.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 12/9/2012 (Lima), 6 901 miembros; 115 publicaciones el último mes. Su descripción permite ofertas laborales para desarrolladores.
    id: "fb-desarrolladores-peru",
    nombre: "Desarrolladores Per\xFA",
    area: "programacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/423231534407524",
    tema: "Desarrollo de software",
    detalle: "Grupo p\xFAblico de Facebook de desarrolladores en Per\xFA (casi 7 000 miembros, desde 2012). Su descripci\xF3n permite ofertas laborales para desarrolladores.",
    revisado: "10 de octubre de 2026"
  },
  // ---------- Educación (canales peruanos de Telegram, activos; la mitad es de inicial)
  {
    id: "mundo-inicial",
    nombre: "Mundo Inicial",
    area: "educacion",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/MundoInicial",
    tema: "Docentes de inicial",
    detalle: "Sitio para maestras de educaci\xF3n inicial (solo avisos)."
  },
  {
    id: "educar-peru",
    nombre: "Educar Per\xFA",
    area: "educacion",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/educarperu",
    tema: "Educaci\xF3n en general",
    detalle: "Canal con informaci\xF3n relacionada al \xE1mbito educativo (solo avisos)."
  },
  {
    // Portal de noticias de educación; su propia web (educacionenred.pe) enlaza este canal. Publica por un servicio de reenvío (enlaces ift.tt).
    id: "educacion-en-red",
    nombre: "Educaci\xF3n en Red",
    area: "educacion",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/educacionenred_noticias",
    tema: "Noticias para docentes",
    detalle: "Canal del portal Educaci\xF3n en Red: noticias del Minedu, bono docente, nombramiento y cronogramas (solo avisos)."
  },
  // ---------- Educación en Facebook (10/10/2026): se abrió la página pública de cada grupo (sin iniciar sesión) y se leyó «Información» y su actividad.
  {
    // Público, creado el 9/3/2019, 62 558 miembros; 9 publicaciones el día de la revisión y 246 en el último mes. Hay avisos de venta de material de sus miembros.
    id: "fb-educacion-inicial-peru",
    nombre: "Educaci\xF3n Inicial - Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/Educacioninicialperu",
    tema: "Educaci\xF3n Inicial",
    detalle: "Grupo p\xFAblico de Facebook de maestras y maestros de educaci\xF3n inicial del Per\xFA (m\xE1s de 62 000 miembros). Algunos miembros publican material a la venta.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 2/4/2014 (Lince, Lima), 4 744 miembros; 9 publicaciones el día de la revisión y 119 en el último mes. La administradora y el Conadis publican.
    id: "fb-educacion-especial-e-inclusiva",
    nombre: "PER\xDA: Educaci\xF3n Especial e Inclusiva",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/759478337405042",
    tema: "Educaci\xF3n Especial",
    detalle: "Grupo p\xFAblico de Facebook sobre educaci\xF3n especial e inclusiva en el Per\xFA (m\xE1s de 4 700 miembros): noticias, normas y avisos del Conadis.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 16/11/2021, 62 428 miembros; 1 009 publicaciones el último mes. Lo administran dos marcas de material educativo; sus reglas permiten publicidad solo de tema educativo.
    id: "fb-docentes-de-inicial",
    nombre: "Docentes de Inicial (todo el Per\xFA)",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/docentesdeinicialperu",
    tema: "Educaci\xF3n Inicial",
    detalle: "Grupo p\xFAblico de Facebook de docentes de inicial de todo el Per\xFA (m\xE1s de 62 000 miembros). Se permite publicidad educativa de sus administradores y miembros.",
    administra: "Aula Activa y Jaquematicas (material educativo)",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 20/5/2023, 11 410 miembros; 113 publicaciones el último mes. Sus reglas prohíben ventas, autopromoción y spam. También difunde gestiones ante el Congreso.
    id: "fb-pronoei",
    nombre: "Grupo Impulsor Nacional de PRONOEI",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/261442202960718",
    tema: "PRONOEI (inicial)",
    detalle: "Grupo p\xFAblico de Facebook de coordinadoras y promotoras de los PRONOEI, programas de educaci\xF3n inicial no escolarizada (m\xE1s de 11 000 miembros). Sus reglas proh\xEDben ventas y spam.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 26/2/2015, 4 304 miembros; 20 publicaciones el último mes. Su regla dice «interaprendizaje sin fines de lucro». El nombre cita al MINEDU y a la UGEL Huancayo, pero no se confirmó que sea oficial.
    id: "fb-especialista-inicial-huancayo",
    nombre: "Especialista de Educaci\xF3n Inicial MINEDU UGEL Huancayo",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/791554954270991",
    tema: "Educaci\xF3n Inicial",
    detalle: "Grupo p\xFAblico de Facebook de interaprendizaje sin fines de lucro para maestras de inicial (m\xE1s de 4 000 miembros). No se confirm\xF3 que sea oficial del MINEDU.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 2/10/2020, 3 079 miembros; 14 publicaciones el último mes (poca actividad). Habla de EBE (educación básica especial) y de los SAANEE del Perú.
    id: "fb-educacion-inclusiva-peru",
    nombre: "Educaci\xF3n Inclusiva - Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/656352795284146",
    tema: "Educaci\xF3n Especial",
    detalle: "Grupo p\xFAblico de Facebook sobre inclusi\xF3n y educaci\xF3n b\xE1sica especial en el Per\xFA (m\xE1s de 3 000 miembros). Publica poco: unas 14 publicaciones al mes.",
    revisado: "10 de octubre de 2026"
  },
  // Docentes y maestros del Perú en general (13/10/2026, «más grupos de educación»): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 19/8/2017, 57 941 miembros; 272 publicaciones el último mes; lo administra una cuenta con su mismo nombre y 2 más.
    id: "fb-entre-maestros-peruanos",
    nombre: "Entre Maestros Peruanos",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/entremaestrosperuanos",
    tema: "Maestros del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook exclusivo de maestros peruanos, con m\xE9todos de ense\xF1anza y t\xE9cnicas de estudio (casi 58 000 miembros, 272 publicaciones al mes, desde 2017).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/3/2018, 236 619 miembros; 242 publicaciones el último mes; lo administran «Materiales del docente» y 6 más. El nombre dice MINEDU pero NO se confirmó que sea oficial.
    id: "fb-peru-educa-docentes",
    nombre: "Per\xFA Educa (MINEDU)",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/docentesperueduca",
    tema: "Docentes del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook de docentes (m\xE1s de 236 000 miembros, 242 publicaciones al mes, desde 2018). Su nombre cita al MINEDU, pero lo administra \xABMateriales del docente\xBB: no es oficial.",
    administra: "la cuenta \xABMateriales del docente\xBB y 6 m\xE1s",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 16/11/2021, 29 977 miembros; 777 publicaciones el último mes; lo administran Aula Activa y Jaquematicas (marcas de material educativo).
    id: "fb-docentes-primaria-peru",
    nombre: "Docentes de Primaria (todo el Per\xFA)",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/docentesdeprimariaperu",
    tema: "Educaci\xF3n Primaria",
    detalle: "Grupo p\xFAblico de Facebook de y para docentes de primaria (unos 30 000 miembros, 777 publicaciones al mes, desde 2021). Sus reglas aceptan publicidad educativa moderada.",
    administra: "Aula Activa y Jaquematicas (material educativo)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 30/10/2016, 26 461 miembros; 1 400 publicaciones el último mes; lo administran «Educare CIC» y más cuentas.
    id: "fb-docentes-peruanos",
    nombre: "Docentes Peruanos",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/194347394351619",
    tema: "Docentes del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook para la comunicaci\xF3n entre docentes del Per\xFA y del mundo (m\xE1s de 26 000 miembros, 1 400 publicaciones al mes, desde 2016). Lo administra \xABEducare CIC\xBB y otras cuentas.",
    administra: "la cuenta \xABEducare CIC\xBB y otras",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 28/7/2019 (nombre cambiado el 18/2/2025), 17 344 miembros; 142 publicaciones el último mes; lo administran «Normas Educativas» y 16 más.
    id: "fb-profesores-del-peru",
    nombre: "Profesores del Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/434031793851211",
    tema: "Profesores del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook de profesores del Per\xFA, \xABun espacio de unidad y crecimiento\xBB (unos 17 300 miembros, 142 publicaciones al mes, desde 2019).",
    administra: "la cuenta \xABNormas Educativas\xBB y 16 m\xE1s",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 26/3/2021 (nombre cambiado el 24/4/2023), 2 564 miembros; 43 publicaciones el último mes; lo administran «Apuntes Del Docente» y «Julio».
    id: "fb-somos-maestros-peru",
    nombre: "Somos los Maestros del Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/471054700751515",
    tema: "Noticias docentes",
    detalle: "Grupo p\xFAblico de Facebook de noticias e informaci\xF3n para docentes del Per\xFA (unos 2 600 miembros, 43 publicaciones al mes, desde 2021).",
    administra: "la cuenta \xABApuntes Del Docente\xBB y 1 m\xE1s",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 12/8/2015 (nombre cambiado el 13/10/2020), 26 333 miembros; 1 724 publicaciones el último mes; lo administra una cuenta llamada «Ong». Descripción: «Recursos para una buena formación docente».
    id: "fb-docentes-del-peru",
    nombre: "Docentes del Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/420214384847704",
    tema: "Docentes del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook con recursos para la formaci\xF3n docente (m\xE1s de 26 000 miembros, 1 724 publicaciones al mes, desde 2015). No pude ver qui\xE9n lo lleva: figura una cuenta llamada \xABOng\xBB.",
    administra: "una cuenta llamada \xABOng\xBB",
    revisado: "13 de octubre de 2026"
  },
  // Docentes de Matemática (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes; no se pudieron ver sus publicaciones.
  {
    // Público, creado el 27/11/2024, 1 955 miembros; 126 publicaciones el último mes.
    id: "fb-docentes-matematica-del-peru",
    nombre: "Docentes de Matem\xE1tica del Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1107487507706806",
    tema: "Docentes de Matem\xE1tica",
    detalle: "Grupo p\xFAblico de Facebook de docentes de matem\xE1tica del Per\xFA (casi 2 000 miembros, 126 publicaciones al mes, desde noviembre de 2024).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 11/4/2023, 2 695 miembros; 66 publicaciones el último mes.
    id: "fb-docentes-matematica-peru",
    nombre: "Docentes de Matem\xE1tica Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/609016281283159",
    tema: "Docentes de Matem\xE1tica",
    detalle: "Grupo p\xFAblico de Facebook de docentes de matem\xE1tica del Per\xFA (unos 2 700 miembros, 66 publicaciones al mes, desde 2023).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 1/4/2023, 3 303 miembros; 75 publicaciones el último mes.
    id: "fb-maestros-matematica-secundaria",
    nombre: "Maestros de Matem\xE1tica Secundaria Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1329682221223841",
    tema: "Matem\xE1tica secundaria",
    detalle: "Grupo p\xFAblico de Facebook de maestros de matem\xE1tica de secundaria del Per\xFA (unos 3 300 miembros, 75 publicaciones al mes, desde 2023).",
    revisado: "13 de octubre de 2026"
  },
  // Docentes de Inglés (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes; no se pudieron ver sus publicaciones.
  {
    // Público, creado el 29/4/2021, 79 114 miembros; 560 publicaciones el último mes.
    id: "fb-profesores-ingles-ebr",
    nombre: "Profesores de Ingl\xE9s del Per\xFA (EBR)",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/475638150304975",
    tema: "Profesores de Ingl\xE9s",
    detalle: "Grupo p\xFAblico de Facebook de profesores de ingl\xE9s de la educaci\xF3n b\xE1sica regular del Per\xFA (unos 79 000 miembros, 560 publicaciones al mes, desde 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 2/6/2022, 2 807 miembros; 284 publicaciones el último mes.
    id: "fb-maestros-ingles-peru",
    nombre: "Maestros de Ingl\xE9s | Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1152011892309885",
    tema: "Maestros de Ingl\xE9s",
    detalle: "Grupo p\xFAblico de Facebook de maestros de ingl\xE9s del Per\xFA (unos 2 800 miembros, 284 publicaciones al mes, desde 2022).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 22/5/2023, 2 997 miembros; 33 publicaciones el último mes.
    id: "fb-docentes-ingles-peru",
    nombre: "Docentes de Ingl\xE9s del Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/145740925070664",
    tema: "Docentes de Ingl\xE9s",
    detalle: "Grupo p\xFAblico de Facebook de docentes de ingl\xE9s del Per\xFA (unos 3 000 miembros, 33 publicaciones al mes, desde 2023).",
    revisado: "13 de octubre de 2026"
  },
  // Comunicación, Ciencia y Tecnología y Ciencias Sociales (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes; no se pudieron ver sus publicaciones.
  {
    // Público, creado el 10/9/2013, 10 952 miembros; 80 publicaciones el último mes.
    id: "fb-docentes-area-comunicacion",
    nombre: "Docentes del \xC1rea de Comunicaci\xF3n",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/docentesdelareadecomunicacion",
    tema: "Docentes de Comunicaci\xF3n",
    detalle: "Grupo p\xFAblico de Facebook de docentes del \xE1rea de Comunicaci\xF3n (casi 11 000 miembros, 80 publicaciones al mes, desde 2013).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 5/5/2021, 4 260 miembros; 200 publicaciones el último mes.
    id: "fb-docentes-comunicacion-peru",
    nombre: "Docentes de Comunicaci\xF3n Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1351357068568093",
    tema: "Docentes de Comunicaci\xF3n",
    detalle: "Grupo p\xFAblico de Facebook de docentes de Comunicaci\xF3n del Per\xFA (unos 4 300 miembros, 200 publicaciones al mes, desde 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 6/4/2021, 3 786 miembros; 159 publicaciones el último mes.
    id: "fb-docentes-cyt-peru",
    nombre: "Docentes CyT Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/3488158487955528",
    tema: "Ciencia y Tecnolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de docentes de Ciencia y Tecnolog\xEDa del Per\xFA (unos 3 800 miembros, 159 publicaciones al mes, desde 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 29/4/2021, 34 480 miembros; 601 publicaciones el último mes.
    id: "fb-maestros-dpcc-ciencias-sociales",
    nombre: "Maestros de DPCC y Ciencias Sociales",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/290558742721721",
    tema: "DPCC y Ciencias Sociales",
    detalle: "Grupo p\xFAblico de Facebook de maestros de Desarrollo Personal, Ciudadan\xEDa y C\xEDvica y de Ciencias Sociales (unos 34 500 miembros, 601 publicaciones al mes, desde 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 2/4/2024, 3 530 miembros; 62 publicaciones el último mes.
    id: "fb-docentes-ccss-dpcc-peru",
    nombre: "Docentes de CCSS y DPCC en Per\xFA",
    area: "educacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/2182025408801333",
    tema: "DPCC y Ciencias Sociales",
    detalle: "Grupo p\xFAblico de Facebook de docentes de Ciencias Sociales y DPCC del Per\xFA (unos 3 500 miembros, 62 publicaciones al mes, desde 2024).",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Derecho
  {
    // No se pudo confirmar desde su web (lpderecho.pe responde 403 a lecturas automáticas): su canal dice «Somos LP» y sus mensajes enlazan lpd.pe.
    id: "lpderecho",
    nombre: "LPderecho",
    area: "derecho",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/lpderechope",
    tema: "Portal jur\xEDdico",
    detalle: "Canal del portal jur\xEDdico LP, que se presenta como \xABel m\xE1s visitado del pa\xEDs\xBB: noticias y webinars de Derecho (solo avisos)."
  },
  // ---------- Derecho en Facebook (10/10/2026): se leyó «Información» y la actividad de la página pública de cada grupo (sin iniciar sesión).
  {
    // Público, creado el 18/4/2020 (etiquetas Cusco, Huancayo, Piura, Madre de Dios), 46 072 miembros; 2 478 publicaciones el último mes. Un aviso a la vista vendía códigos.
    id: "fb-estudiantes-derecho-peru",
    nombre: "Estudiantes de Derecho Per\xFA",
    area: "derecho",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/EstudiantesDerechoPeru",
    tema: "Estudiantes de Derecho",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Derecho del Per\xFA (m\xE1s de 46 000 miembros, unas 2 400 publicaciones al mes). Algunos avisos son de venta de libros.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 25/12/2016, 12 831 miembros; 107 publicaciones el último mes. Lo administra la cuenta «Abogados.pe» (la misma del grupo «Derecho Perú»). Su nombre dice «Oficial», sin institución detrás confirmada.
    id: "fb-estudiantes-derecho-oficial",
    nombre: "Estudiantes de Derecho del Per\xFA",
    area: "derecho",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/estudiantes.derecho.peru.oficial",
    tema: "Estudiantes de Derecho",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Derecho del Per\xFA (m\xE1s de 12 000 miembros). Su nombre dice \xABOficial\xBB, pero no se confirm\xF3 que sea de una instituci\xF3n.",
    administra: "la cuenta \xABAbogados.pe\xBB y 2 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 7/6/2020 (Lima), 13 341 miembros; 518 publicaciones el último mes.
    id: "fb-derecho-peru-abogados",
    nombre: "Derecho Per\xFA (Abogados Per\xFA)",
    area: "derecho",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/derecho.peru.abogados.peru",
    tema: "Abogados y estudiantes",
    detalle: "Grupo p\xFAblico de Facebook de abogados y estudiantes de Derecho del Per\xFA, de Lima (m\xE1s de 13 000 miembros, unas 500 publicaciones al mes).",
    administra: "la cuenta \xABAbogados.pe\xBB y 4 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 1/4/2021, 14 421 miembros; 703 publicaciones el último mes. Un aviso a la vista era una oferta de prácticas.
    id: "fb-estudiantes-derecho-coleguitas",
    nombre: "Estudiantes de Derecho y Coleguitas del Per\xFA",
    area: "derecho",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/4039386389488478",
    tema: "Estudiantes de Derecho",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Derecho del Per\xFA (m\xE1s de 14 000 miembros, unas 700 publicaciones al mes). Tambi\xE9n se publican ofertas de pr\xE1cticas.",
    administra: "la cuenta \xABIncapyc Educa - Derecho\xBB y 2 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 2/5/2014, 3 444 miembros; 228 publicaciones el último mes, 8 administradores. Un aviso a la vista era una convocatoria de practicante.
    id: "fb-abogados-estudiantes-magistrados",
    nombre: "Abogados, Estudiantes de Derecho y Magistrados Peruanos",
    area: "derecho",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/318027595016673",
    tema: "Abogados y estudiantes",
    detalle: "Grupo p\xFAblico de Facebook de abogados, estudiantes y magistrados peruanos (m\xE1s de 3 000 miembros, desde 2014). Tambi\xE9n se publican convocatorias de practicantes.",
    revisado: "10 de octubre de 2026"
  },
  // ---------- Contabilidad
  {
    id: "ccp-ancash",
    nombre: "Colegio de Contadores P\xFAblicos de \xC1ncash",
    area: "contabilidad",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/eventosccpa",
    tema: "Colegio profesional",
    detalle: "Canal de difusi\xF3n sobre las actividades del Colegio de Contadores P\xFAblicos de \xC1ncash (solo avisos).",
    administra: "el colegio profesional",
    oficial: true
    // su cuenta oficial @ccpancash, enlazada en ccpancash.org, apunta a este canal
  },
  // ---------- Contabilidad en Facebook (10/10/2026): se leyó «Información» y la actividad de la página pública de cada grupo (sin iniciar sesión).
  {
    // Público, creado el 20/4/2015, 47 303 miembros; 883 publicaciones el último mes. Su descripción invita a subir archivos (PDF, PPT, Word).
    id: "fb-estudiantes-contabilidad-del-peru",
    nombre: "Estudiantes de Contabilidad del Per\xFA",
    area: "contabilidad",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/773211452798394",
    tema: "Estudiantes de Contabilidad",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Contabilidad del Per\xFA (m\xE1s de 47 000 miembros, unas 880 publicaciones al mes). Su descripci\xF3n invita a subir archivos (PDF, PPT, Word).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 23/7/2017 (etiqueta «Perú»), 58 145 miembros; 119 publicaciones el último mes. Lo administra la página «Perú Contadores y Tecnología»; reglas: sin política ni religión.
    id: "fb-peru-contable",
    nombre: "Grupo Per\xFA Contable",
    area: "contabilidad",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1394944627288331",
    tema: "Contadores y estudiantes",
    detalle: "Grupo p\xFAblico de Facebook, foro de consultas contables, tributarias y laborales para contadores y estudiantes (m\xE1s de 58 000 miembros, desde 2017).",
    administra: "la p\xE1gina \xABPer\xFA Contadores y Tecnolog\xEDa\xBB",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 3/5/2021 (etiquetas de regiones del Perú), 29 518 miembros; 1 239 publicaciones el último mes. Un aviso a la vista era una oferta de prácticas.
    id: "fb-estudiantes-contabilidad-peru-consulta",
    nombre: "Estudiantes de Contabilidad Per\xFA (consulta y comparte)",
    area: "contabilidad",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/588483179211702",
    tema: "Estudiantes de Contabilidad",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Contabilidad de varias regiones del Per\xFA (casi 30 000 miembros, unas 1 200 publicaciones al mes). Tambi\xE9n se publican ofertas de pr\xE1cticas.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 27/7/2020 (etiqueta «Perú»), 14 011 miembros; 81 publicaciones el último mes.
    id: "fb-estudiantes-contabilidad-peru-foro",
    nombre: "Estudiantes de Contabilidad Per\xFA (foro)",
    area: "contabilidad",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/estudiantesdecontabilidadperu",
    tema: "Foro contable y tributario",
    detalle: "Grupo p\xFAblico de Facebook, foro contable, tributario y empresarial para consultar y opinar (14 000 miembros, 81 publicaciones al mes, desde 2020).",
    revisado: "10 de octubre de 2026"
  },
  // ---------- Ambiental y Agronomía
  {
    // No se pudo confirmar desde su web (senamhi.gob.pe no cita el canal): su descripción dice «Organismo adscrito al Minam» y todos sus mensajes enlazan senamhi.gob.pe.
    id: "senamhi",
    nombre: "Senamhi Per\xFA",
    area: "ambiental",
    plataforma: "telegram",
    tipo: "canal",
    url: "https://t.me/Senamhi_Peru",
    tema: "Clima y pron\xF3sticos",
    detalle: "Canal del Senamhi: informaci\xF3n meteorol\xF3gica, hidrol\xF3gica y clim\xE1tica del Per\xFA (solo avisos).",
    administra: "Senamhi (no confirmado desde su web)"
  },
  // ---------- Ambiental y Agronomía en Facebook (10/10/2026): se leyó «Información» y la actividad de la página pública de cada grupo (sin iniciar sesión).
  {
    // Público, creado el 21/1/2018, 64 584 miembros; 1 678 publicaciones el último mes. Facebook lo muestra como «Grupo de Agricultores del MUNDO»; dice «del Perú y del Mundo».
    id: "fb-ingenieros-agronomos-peru-mundo",
    nombre: "Ingenieros Agronomos Per\xFA",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1757687977627949",
    tema: "Agronom\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de ingenieros agr\xF3nomos y profesionales del agro del Per\xFA y del mundo (m\xE1s de 64 000 miembros, unas 1 700 publicaciones al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 8/9/2013 (etiqueta «Perú»), 25 556 miembros; 1 170 publicaciones el último mes.
    id: "fb-ingenieros-agronomos-del-peru",
    nombre: "Ingenieros Agr\xF3nomos del Per\xFA",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/440944936019846",
    tema: "Agronom\xEDa",
    detalle: "Grupo p\xFAblico de Facebook para contribuir al desarrollo del agro peruano (m\xE1s de 25 000 miembros, desde 2013, unas 1 100 publicaciones al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 26/12/2017 (etiquetas Trujillo, Piura, Ica), 28 411 miembros; 90 publicaciones el último mes. Facebook lo muestra como «Grupo de Agroskynet».
    id: "fb-ingenieros-agronomos-peru-agroskynet",
    nombre: "Ingenieros Agronomos Per\xFA (Agroskynet)",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/ingenierosagronomosperu",
    tema: "Agronom\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de profesionales de Ingenier\xEDa Agron\xF3mica del Per\xFA (m\xE1s de 28 000 miembros, desde 2017). Facebook lo muestra ligado a la p\xE1gina \xABAgroskynet\xBB.",
    administra: "la cuenta \xABAgroskynet\xBB y 4 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 21/3/2020, 11 254 miembros; 293 publicaciones el último mes. Tiene la pestaña «Compraventa».
    id: "fb-ingenieros-agronomos-avances",
    nombre: "Ingenieros Agr\xF3nomos del Per\xFA (avances y logros)",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/910632482712576",
    tema: "Agronom\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de ingenieros agr\xF3nomos del Per\xFA (m\xE1s de 11 000 miembros, desde 2020) para presentar avances tecnol\xF3gicos y logros. Tiene una pesta\xF1a de compraventa.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 13/4/2020, 30 595 miembros; 153 publicaciones el último mes. Facebook lo muestra como «Grupo de Ingeniería Ambiental Perú»; administra «Profesionales Ambientales Unidos-PAU» y 8 más. Tiene la pestaña «Compraventa».
    id: "fb-ingenieros-ambientales-peru",
    nombre: "Ingenieros Ambientales de Per\xFA",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/661043621388036",
    tema: "Ingenier\xEDa Ambiental",
    detalle: "Grupo p\xFAblico de Facebook de Ingenier\xEDa Ambiental del Per\xFA (m\xE1s de 30 000 miembros, desde 2020). Tiene una pesta\xF1a de compraventa y varios avisos de empleo.",
    administra: "la cuenta \xABProfesionales Ambientales Unidos-PAU\xBB y 8 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 7/12/2016, 5 250 miembros; 102 publicaciones el último mes. Un aviso a la vista era una oferta de prácticas.
    id: "fb-red-profesionales-ing-ambiental",
    nombre: "Red de Profesionales de Ing. Ambiental - Per\xFA",
    area: "ambiental",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1743854785935019",
    tema: "Ingenier\xEDa Ambiental",
    detalle: "Grupo p\xFAblico de Facebook de profesionales y estudiantes de Ingenier\xEDa Ambiental del Per\xFA (m\xE1s de 5 000 miembros, desde 2016). Tambi\xE9n se publican ofertas de pr\xE1cticas.",
    revisado: "10 de octubre de 2026"
  },
  // ---------- Ingeniería
  {
    id: "cip-cn",
    nombre: "Colegio de Ingenieros del Per\xFA (CIP-CN)",
    area: "ingenieria",
    plataforma: "whatsapp",
    tipo: "canal",
    url: "https://whatsapp.com/channel/0029VbDGiNODZ4Ldfe0RO11y",
    tema: "Colegio profesional",
    detalle: "Canal de WhatsApp del Colegio de Ingenieros del Per\xFA (Consejo Nacional), que su propia web promueve (solo avisos).",
    administra: "el colegio profesional",
    oficial: true
    // lo promueve cip.org.pe
  },
  // ---------- Ingeniería en Facebook (10/10/2026): se leyó «Información» y la actividad de la página pública de cada grupo (sin iniciar sesión).
  {
    // Público, creado el 22/3/2014, 6 512 miembros; 146 publicaciones el último mes. Facebook lo muestra como «Grupo de Red Mundial de Expertos».
    id: "fb-estudiantes-ingenieria-peru",
    nombre: "Estudiantes de Ingenier\xEDa en el Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/289513784536893",
    tema: "Todas las ingenier\xEDas",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de ingenier\xEDa del Per\xFA (m\xE1s de 6 000 miembros, desde 2014). Facebook lo muestra ligado a la p\xE1gina \xABRed Mundial de Expertos\xBB.",
    administra: "la p\xE1gina \xABRed Mundial de Expertos\xBB",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 9/6/2014 (Lima), 43 200 miembros; 858 publicaciones el último mes. 1 administrador y 5 moderadores. Un aviso a la vista era una búsqueda de empleo.
    id: "fb-estudiante-ingenieria-civil-peru",
    nombre: "Estudiante de Ingenier\xEDa Civil Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1383484105274767",
    tema: "Ingenier\xEDa Civil",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Ingenier\xEDa Civil de Lima y el Per\xFA (m\xE1s de 43 000 miembros, unas 850 publicaciones al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 16/12/2020, 13 452 miembros; 912 publicaciones el último mes.
    id: "fb-ingenieros-civiles-peru",
    nombre: "Ingenieros Civiles Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/388173345940220",
    tema: "Ingenier\xEDa Civil",
    detalle: "Grupo p\xFAblico de Facebook para compartir experiencias y material de Ingenier\xEDa Civil en el Per\xFA (m\xE1s de 13 000 miembros, unas 900 publicaciones al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 20/2/2016 (etiquetas de regiones del Perú: Puno, Cusco, Lima, Ica), 193 313 miembros; 2 443 publicaciones el último mes. Facebook lo muestra como «Grupo de MetalCad Ingenieros»; su nombre no dice «Perú».
    id: "fb-ingenieria-mecanica",
    nombre: "Ingenier\xEDa Mec\xE1nica",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/ing.mecanic",
    tema: "Ingenier\xEDa Mec\xE1nica",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes y profesionales de Ingenier\xEDa Mec\xE1nica (m\xE1s de 190 000 miembros). Su nombre no dice \xABPer\xFA\xBB, pero sus lugares son regiones peruanas.",
    administra: "la p\xE1gina \xABMetalCad Ingenieros\xBB y 3 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 16/8/2011, 20 215 miembros; 480 publicaciones el último mes. Su descripción permite solicitudes de empleo y promociones.
    id: "fb-ingenieros-electricistas-peru",
    nombre: "Ingenieros Electricistas del Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/Peru.Fiee",
    tema: "Ingenier\xEDa El\xE9ctrica",
    detalle: "Grupo p\xFAblico de Facebook de Ingenier\xEDa El\xE9ctrica (m\xE1s de 20 000 miembros, desde 2011): charlas, conferencias y avances. Tambi\xE9n se permiten pedidos de empleo y promociones.",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 14/4/2020 (Perú, Lima), 21 964 miembros; 745 publicaciones el último mes. Su descripción permite oportunidades laborales y promoción de empresas.
    id: "fb-ingenieros-tecnicos-electricistas-peru",
    nombre: "Ingenieros y T\xE9cnicos Electricistas del Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/533317587382920",
    tema: "Ingenier\xEDa El\xE9ctrica",
    detalle: "Grupo p\xFAblico de Facebook de ingenieros y t\xE9cnicos electricistas del Per\xFA (casi 22 000 miembros). Se permiten oportunidades laborales y promoci\xF3n de empresas.",
    administra: "la p\xE1gina \xABGlobal Per\xFA\xBB y 1 m\xE1s",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 5/2/2021 (etiqueta «Perú»), 25 227 miembros; 555 publicaciones el último mes. Su nombre dice «Oficial», sin institución detrás confirmada; es «la familia de mineros del Perú y del mundo».
    id: "fb-ingenieria-de-minas",
    nombre: "Ingenier\xEDa de Minas",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/137040841571432",
    tema: "Ingenier\xEDa de Minas",
    detalle: "Grupo p\xFAblico de Facebook de mineros del Per\xFA y del mundo (m\xE1s de 25 000 miembros). Su nombre dice \xABOficial\xBB, pero no se confirm\xF3 que sea de una instituci\xF3n.",
    administra: "la cuenta \xABIngenier\xEDa de Minas - Salvatierra\xBB",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 29/12/2022, 3 136 miembros; 299 publicaciones el último mes.
    id: "fb-ingenieros-de-minas-peru",
    nombre: "Ingenieros de Minas del Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/490956959829346",
    tema: "Ingenier\xEDa de Minas",
    detalle: "Grupo p\xFAblico de Facebook para compartir temas de la profesi\xF3n de Ingenier\xEDa de Minas en el Per\xFA (m\xE1s de 3 000 miembros, unas 300 publicaciones al mes).",
    revisado: "10 de octubre de 2026"
  },
  {
    // Público, creado el 3/9/2023, 3 657 miembros; 152 publicaciones el último mes. Su descripción se presenta como «el grupo #1» (no verificable).
    id: "fb-ingenieros-industriales-peru",
    nombre: "Ingenieros Industriales Per\xFA",
    area: "ingenieria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/551565847095162",
    tema: "Ingenier\xEDa Industrial",
    detalle: "Grupo p\xFAblico de Facebook de Ingenier\xEDa Industrial del Per\xFA (m\xE1s de 3 600 miembros, desde 2023). Se presenta como \xABel grupo #1\xBB, algo que no se puede comprobar.",
    revisado: "10 de octubre de 2026"
  },
  // ---------- Administración (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. Los tres traen avisos de cursos de pago de un centro de capacitación.
  {
    // Público, creado el 28/2/2021, 9 950 miembros; 769 publicaciones el último mes. La publicación que se vio era un aviso de un curso de pago (CECAF).
    id: "fb-estudiantes-contabilidad-administracion-peru",
    nombre: "Estudiantes de Contabilidad y Administraci\xF3n Per\xFA",
    area: "administracion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/2303496619794063",
    tema: "Administraci\xF3n y Contabilidad",
    detalle: "Grupo p\xFAblico de Facebook (unos 10 000 miembros, 769 publicaciones al mes) para consultas, trabajos y pr\xE1cticas. Se ven avisos de cursos de pago de un centro de capacitaci\xF3n.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 31/10/2015, 1 711 miembros; 100 publicaciones el último mes. La publicación que se vio era un video promocional de TikTok.
    id: "fb-estudiantes-administracion-contabilidad-peru",
    nombre: "Estudiantes de Administraci\xF3n y Contabilidad en el Per\xFA",
    area: "administracion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1502685973390898",
    tema: "Administraci\xF3n y Contabilidad",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de Administraci\xF3n y Contabilidad (unos 1 700 miembros, 100 publicaciones al mes, desde 2015). Se ven publicaciones de promoci\xF3n de cursos.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 16/7/2022, 1 400 miembros; 68 publicaciones el último mes. La publicación que se vio era un aviso de un curso de pago (CECAF).
    id: "fb-administradores-del-peru",
    nombre: "Administradores del Per\xFA",
    area: "administracion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/422134813176090",
    tema: "Administraci\xF3n (profesionales)",
    detalle: "Grupo p\xFAblico de Facebook de profesionales de la administraci\xF3n del Per\xFA (unos 1 400 miembros, 68 publicaciones al mes): experiencias, ofertas laborales y avisos de cursos de pago.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Veterinaria (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes.
  {
    // Público, creado el 12/5/2014, 2 778 miembros; 56 publicaciones el último mes; administran «Mv» y «Jessica». No se pudieron ver sus publicaciones (la página pide iniciar sesión).
    id: "fb-peru-colegas-veterinarios",
    nombre: "Per\xFA Colegas Veterinarios",
    area: "veterinaria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/mvzo.peru",
    tema: "Medicina Veterinaria",
    detalle: "Grupo p\xFAblico de Facebook para debatir casos entre colegas veterinarios del Per\xFA (m\xE1s de 2 700 miembros, 56 publicaciones al mes, desde 2014). No se pudieron ver sus publicaciones.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Trabajo Social (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 8/6/2012, 12 323 miembros; 348 publicaciones el último mes.
    id: "fb-trabajo-social-peru-red",
    nombre: "Trabajo Social Per\xFA (red de trabajadores sociales)",
    area: "trabajosocial",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/anaetsperu",
    tema: "Trabajo Social",
    detalle: "Grupo p\xFAblico de Facebook, \xABred de trabajadores sociales\xBB para compartir informaci\xF3n (m\xE1s de 12 000 miembros, 348 publicaciones al mes, desde 2012). No se pudieron ver sus publicaciones.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 30/3/2022 (Perú), 1 749 miembros; 123 publicaciones el último mes.
    id: "fb-trabajo-social-peru-conocimientos",
    nombre: "Trabajo Social Per\xFA (conocimientos y dudas)",
    area: "trabajosocial",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/657270618873715",
    tema: "Trabajo Social",
    detalle: "Grupo p\xFAblico de Facebook donde trabajadores sociales comparten conocimientos y dudas (unos 1 700 miembros, 123 publicaciones al mes, desde 2022). No se pudieron ver sus publicaciones.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Marketing (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 12/3/2015, 40 736 miembros; 573 publicaciones el último mes. Un resultado de búsqueda mostró el pedido de prácticas de una estudiante de SENATI.
    id: "fb-marketing-peru",
    nombre: "Marketing Per\xFA",
    area: "marketing",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1561532690796567",
    tema: "Marketing",
    detalle: "Grupo p\xFAblico de Facebook sobre marketing (m\xE1s de 40 000 miembros, 573 publicaciones al mes, desde 2015). Entre sus publicaciones hay pedidos de pr\xE1cticas y de empleo.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Perú, Piura), creado el 29/10/2014, 2 709 miembros; 138 publicaciones el último mes. Un resultado de búsqueda mostró una oferta de trabajo.
    id: "fb-community-manager-peru",
    nombre: "Marketing de Redes Sociales - Community Manager Per\xFA",
    area: "marketing",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/communitymanagerperu",
    tema: "Redes sociales y marketing",
    detalle: "Grupo p\xFAblico de Facebook de marketing en redes sociales y community managers del Per\xFA (unos 2 700 miembros, 138 publicaciones al mes, desde 2014). Se ven ofertas de trabajo.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Psicología (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. Se crearon ANTES de 2020 (2010-2019): el dueño decidió cargarlos igual por estar activos. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 2/6/2010, 52 261 miembros; 1 678 publicaciones el último mes.
    id: "fb-psicologos-peru-todos",
    nombre: "Psic\xF3logos Per\xFA (todos los psic\xF3logos del pa\xEDs)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/psicologoslimaperu",
    tema: "Psicolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de psic\xF3logos del Per\xFA (m\xE1s de 52 000 miembros, unas 1 700 publicaciones al mes, desde 2010). Su descripci\xF3n dice que re\xFAne a todos los psic\xF3logos del pa\xEDs.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 6/9/2015, 22 210 miembros; 734 publicaciones el último mes.
    id: "fb-psicologos-peruanos",
    nombre: "Psic\xF3logos Peruanos",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/psicologosperuanos",
    tema: "Psicolog\xEDa peruana",
    detalle: "Grupo p\xFAblico de Facebook para compartir experiencias de la psicolog\xEDa peruana (m\xE1s de 22 000 miembros, 734 publicaciones al mes, desde 2015).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Lima), creado el 20/11/2019, 27 972 miembros; 632 publicaciones el último mes.
    id: "fb-psicologas-psicologos-estudiantes-lima",
    nombre: "Psic\xF3logas, Psic\xF3logos y Estudiantes de Psicolog\xEDa (Lima)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/ciapse.lima",
    tema: "Psic\xF3logos y estudiantes",
    detalle: "Grupo p\xFAblico de Facebook de psic\xF3logos y estudiantes de psicolog\xEDa de Lima, Per\xFA (casi 28 000 miembros, 632 publicaciones al mes, desde noviembre de 2019).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 27/10/2013, 18 859 miembros; 233 publicaciones el último mes. Su descripción pide a los centros que dejan publicidad de cursos y talleres que compartan artículos.
    id: "fb-psicologos-peru-articulos",
    nombre: "Psic\xF3logos Per\xFA (art\xEDculos y talleres)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/psicologosperu",
    tema: "Psicolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de psic\xF3logos del Per\xFA (casi 19 000 miembros, 233 publicaciones al mes, desde 2013). Pide a los centros que anuncian cursos y talleres que compartan tambi\xE9n art\xEDculos.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/8/2016, 17 880 miembros; 1 711 publicaciones el último mes. Su descripción dice que está abierto a la difusión de eventos y servicios académicos.
    id: "fb-psicologia-peru",
    nombre: "Psicolog\xEDa Per\xFA",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/628385087337726",
    tema: "Psicolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook abierto a la difusi\xF3n de eventos y servicios acad\xE9micos de la psicolog\xEDa (casi 18 000 miembros, m\xE1s de 1 700 publicaciones al mes, desde 2016). Hay mucha publicidad.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/4/2017, 10 397 miembros; 201 publicaciones el último mes. El nombre dice «Oficial» sin institución.
    id: "fb-psicologos-peru-oficial",
    nombre: "Psic\xF3logos Per\xFA Oficial (psicolog\xEDa y psicoterapia)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/psicologiaperu",
    tema: "Psicolog\xEDa y psicoterapia",
    detalle: "Grupo p\xFAblico de Facebook solo de mensajes de psicolog\xEDa y psicoterapia (m\xE1s de 10 000 miembros, 201 publicaciones al mes, desde 2017). Su nombre dice \xABOficial\xBB, pero no se confirm\xF3 que lo sea.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 18/6/2018, 6 168 miembros; 30 publicaciones el último mes. Solo admite temas de psicología clínica; menciona a ANEPSI.
    id: "fb-psicologia-estudiantes-egresados-clinica",
    nombre: "Estudiantes y Egresados de Psicolog\xEDa (\xE1rea cl\xEDnica)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1838935806409388",
    tema: "Psicolog\xEDa cl\xEDnica",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes y egresados de psicolog\xEDa solo de temas de psicolog\xEDa cl\xEDnica (m\xE1s de 6 000 miembros, 30 publicaciones al mes, desde 2018; menciona a ANEPSI Per\xFA).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 3/5/2017, 3 393 miembros; 50 publicaciones el último mes. Su descripción es compartir eventos y capacitaciones.
    id: "fb-psicologos-del-peru-eventos",
    nombre: "Psic\xF3logos del Per\xFA (eventos y capacitaciones)",
    area: "psicologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/442997866047493",
    tema: "Eventos y capacitaciones",
    detalle: "Grupo p\xFAblico de Facebook para compartir eventos y capacitaciones de desarrollo humano (m\xE1s de 3 000 miembros, 50 publicaciones al mes, desde 2017). Son sobre todo anuncios de cursos.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Enfermería (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público (Cusco), creado el 23/4/2020, 1 756 miembros; 119 publicaciones el último mes.
    id: "fb-estudiantes-enfermeria-peru",
    nombre: "Estudiantes de Enfermer\xEDa Per\xFA",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/EstudiantesdeEnfermeriaPeru",
    tema: "Estudiantes de Enfermer\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de enfermer\xEDa del Per\xFA (m\xE1s de 1 700 miembros, 119 publicaciones al mes, desde abril de 2020).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/6/2020, 9 565 miembros; 703 publicaciones el último mes.
    id: "fb-enfermeria-peru-2026",
    nombre: "Enfermer\xEDa Per\xFA 2026",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/580004539580637",
    tema: "Enfermer\xEDa",
    detalle: "Grupo p\xFAblico de Facebook que busca reunir a las colegas de enfermer\xEDa del Per\xFA (m\xE1s de 9 000 miembros, 703 publicaciones al mes, desde junio de 2020).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 28/1/2021, 12 107 miembros; 706 publicaciones el último mes.
    id: "fb-licenciados-enfermeria-peru",
    nombre: "Licenciados de Enfermer\xEDa en Per\xFA",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/licenciadosenfermeros",
    tema: "Licenciados de Enfermer\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de licenciados de enfermer\xEDa del Per\xFA (m\xE1s de 12 000 miembros, 706 publicaciones al mes, desde enero de 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Lima), creado el 18/5/2021, 2 487 miembros; 89 publicaciones el último mes.
    id: "fb-estudiantes-medicina-enfermeria-peru",
    nombre: "Estudiantes de Medicina y Enfermer\xEDa del Per\xFA",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/117151240431410",
    tema: "Medicina y Enfermer\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de medicina y enfermer\xEDa del Per\xFA (unos 2 500 miembros, 89 publicaciones al mes, desde mayo de 2021; Lima).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Lima), creado el 12/5/2020, 2 230 miembros; 38 publicaciones el último mes. Se presenta como espacio de educación continua.
    id: "fb-enfermeria-peru-educacion-continua",
    nombre: "Enfermer\xEDa Per\xFA - Educaci\xF3n continua",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/864930487322119",
    tema: "Educaci\xF3n continua",
    detalle: "Grupo p\xFAblico de Facebook que se presenta como espacio de educaci\xF3n continua para enfermer\xEDa (m\xE1s de 2 200 miembros, 38 publicaciones al mes, desde mayo de 2020; Lima).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 14/4/2017 (ANTES de 2020), 5 049 miembros; 206 publicaciones el último mes.
    id: "fb-estudiantes-enfermeria-proyecto-lima",
    nombre: "Estudiantes de Enfermer\xEDa - Proyecto Lima",
    area: "enfermeria",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/230265500783581",
    tema: "Estudiantes de Enfermer\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de enfermer\xEDa para compartir informaci\xF3n (m\xE1s de 5 000 miembros, 206 publicaciones al mes). Se cre\xF3 en 2017, antes de 2020.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Medicina (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 7/11/2022, 5 266 miembros; 203 publicaciones el último mes. El nombre dice «(GRUPO OFICIAL)» sin institución.
    id: "fb-medicina-humana-peru-oficial",
    nombre: "Medicina Humana Per\xFA (portal de la medicina peruana)",
    area: "medicina",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/medicinahumanaperuoficial",
    tema: "Medicina Humana",
    detalle: "Grupo p\xFAblico de Facebook sobre medicina humana en el Per\xFA (m\xE1s de 5 000 miembros, 203 publicaciones al mes, desde noviembre de 2022). Su nombre dice \xABGrupo oficial\xBB, pero no se confirm\xF3 de qui\xE9n es.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 27/4/2010 (ANTES de 2020), 40 897 miembros; 91 publicaciones el último mes. Dice ser el mayor grupo de Facebook de médicos y estudiantes de medicina del Perú.
    id: "fb-red-peruana-medico-joven",
    nombre: "Red Peruana del M\xE9dico Joven",
    area: "medicina",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/medicojoven",
    tema: "M\xE9dicos y estudiantes",
    detalle: "Grupo p\xFAblico de Facebook de m\xE9dicos y estudiantes de medicina del Per\xFA (casi 41 000 miembros, 91 publicaciones al mes). Se cre\xF3 en 2010, antes de 2020.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Negocios Internacionales y comercio exterior (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 21/4/2025, 1 903 miembros; 67 publicaciones el último mes. Un resultado de búsqueda mostró una oferta de empleo.
    id: "fb-ni-comercio-exterior-peru",
    nombre: "Negocios Internacionales y Comercio Exterior Per\xFA",
    area: "negociosint",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/708563764849216",
    tema: "Negocios Internacionales",
    detalle: "Grupo p\xFAblico de Facebook de negocios internacionales y comercio exterior del Per\xFA (casi 1 900 miembros, 67 publicaciones al mes, desde abril de 2025). Se ven ofertas de empleo.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 7/1/2021, 3 272 miembros; 86 publicaciones el último mes.
    id: "fb-peru-comercio-exterior",
    nombre: "Per\xFA - Comercio exterior (importaci\xF3n y exportaci\xF3n)",
    area: "negociosint",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/3567843126598821",
    tema: "Comercio exterior",
    detalle: "Grupo p\xFAblico de Facebook para orientar a quienes no conocen lo b\xE1sico de importar y exportar en el Per\xFA (unos 3 300 miembros, 86 publicaciones al mes, desde enero de 2021).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/10/2015 (ANTES de 2020), 5 280 miembros; 153 publicaciones el último mes.
    id: "fb-comercio-exterior-importacion-exportacion-aduanas",
    nombre: "Comercio exterior (importaci\xF3n, exportaci\xF3n y aduanas) Per\xFA",
    area: "negociosint",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/176139452725766",
    tema: "Comercio exterior y aduanas",
    detalle: "Grupo p\xFAblico de Facebook para aprender de comercio internacional, importaciones, exportaciones y aduanas en el Per\xFA (m\xE1s de 5 000 miembros, 153 publicaciones al mes, desde 2015).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 17/11/2015 (ANTES de 2020), 9 575 miembros; 63 publicaciones el último mes.
    id: "fb-aduanas-logistica-comercio-exterior",
    nombre: "Aduanas, Log\xEDstica y Comercio Exterior - Per\xFA",
    area: "negociosint",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/195071037494910",
    tema: "Aduanas y log\xEDstica",
    detalle: "Grupo p\xFAblico de Facebook para interesados en comercio exterior y aduanas que quieren compartir art\xEDculos de la carrera (casi 9 600 miembros, 63 publicaciones al mes, desde 2015).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Miraflores, Lima), creado el 2/9/2015 (ANTES de 2020), 20 429 miembros; 34 publicaciones el último mes.
    id: "fb-comercio-exterior-aduanas-profesionales",
    nombre: "Comercio exterior y aduanas, profesionales Per\xFA",
    area: "negociosint",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/505445602942845",
    tema: "Profesionales de aduanas",
    detalle: "Grupo p\xFAblico de Facebook de especialistas en negocios internacionales y aduanas, importadores y exportadores (m\xE1s de 20 000 miembros, 34 publicaciones al mes, desde 2015; Lima).",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Economía (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público (Perú), creado el 3/6/2012 (ANTES de 2020), 81 123 miembros; 56 publicaciones el último mes.
    id: "fb-economia-peru",
    nombre: "Econom\xEDa Per\xFA (opini\xF3n e informaci\xF3n econ\xF3mica)",
    area: "economia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/ECONOMIAPERU",
    tema: "Econom\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de opini\xF3n, propuestas e informaci\xF3n en econom\xEDa para profesionales y estudiantes (m\xE1s de 81 000 miembros, 56 publicaciones al mes, desde 2012).",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Arquitectura (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión); varios son de servicios de ayuda a estudiantes y lo dicen.
  {
    // Público, creado el 11/4/2021, 16 036 miembros; 597 publicaciones el último mes. Etiqueta «proveedores de servicios».
    id: "fb-arquitectos-lima-peru",
    nombre: "Arquitectos Lima Per\xFA (arquitectos, ingenieros y construcci\xF3n)",
    area: "arquitectura",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/189659069465860",
    tema: "Arquitectos y construcci\xF3n",
    detalle: "Grupo p\xFAblico de Facebook de arquitectos, ingenieros y profesionales de la construcci\xF3n, peruano e internacional (16 000 miembros, 597 publicaciones al mes, desde abril de 2021). Hay proveedores de servicios.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público (Lima), creado el 7/12/2013 (ANTES de 2020), 14 423 miembros; 37 publicaciones el último mes.
    id: "fb-red-arquitectos-peruanos",
    nombre: "Red de Arquitectos Peruanos",
    area: "arquitectura",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/reddearquitectosperuanos",
    tema: "Arquitectos peruanos",
    detalle: "Grupo p\xFAblico de Facebook exclusivo para profesionales y estudiantes de arquitectura del Per\xFA (m\xE1s de 14 000 miembros, 37 publicaciones al mes, desde 2013; Lima).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/11/2022, 2 558 miembros; 199 publicaciones el último mes. Resultados de búsqueda mostraron anuncios de ayuda con entregas y de becas.
    id: "fb-arquitectura-estudiantes-peru",
    nombre: "Arquitectura - Estudiantes Per\xFA",
    area: "arquitectura",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/512330420911972",
    tema: "Estudiantes de Arquitectura",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de arquitectura del Per\xFA (unos 2 600 miembros, 199 publicaciones al mes, desde noviembre de 2022). Se ven anuncios de ayuda con entregas y de becas.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 31/7/2024, 1 746 miembros; 249 publicaciones el último mes. Su descripción dice que es un staff de profesionales al servicio de estudiantes (asesoría en entregas de taller).
    id: "fb-estudiantes-arquitectura-peru-ayuda",
    nombre: "Estudiantes de Arquitectura Per\xFA (ayuda con entregas)",
    area: "arquitectura",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/463782709855310",
    tema: "Ayuda con entregas",
    detalle: "Grupo p\xFAblico de Facebook de un equipo de profesionales que ayuda o asesora a estudiantes en sus entregas de taller (m\xE1s de 1 700 miembros, 249 publicaciones al mes, desde julio de 2024). Es un servicio.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 11/10/2014 (ANTES de 2020), 2 690 miembros; 91 publicaciones el último mes. Un resultado de búsqueda mostró un aviso de servicios.
    id: "fb-estudiantes-arquitectura-peru",
    nombre: "Estudiantes de Arquitectura Per\xFA",
    area: "arquitectura",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1562759787286762",
    tema: "Estudiantes de Arquitectura",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de arquitectura del Per\xFA (unos 2 700 miembros, 91 publicaciones al mes, desde 2014). Se ven avisos de servicios.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Odontología (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 3/4/2023, 3 424 miembros; 234 publicaciones el último mes.
    id: "fb-estudiante-odontologia-peru",
    nombre: "Estudiante de Odontolog\xEDa del Per\xFA",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/estudiantedeodontologiadelperu",
    tema: "Estudiantes de Odontolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de odontolog\xEDa del Per\xFA, de pre y posgrado (unos 3 400 miembros, 234 publicaciones al mes, desde abril de 2023).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 22/5/2024, 6 608 miembros; 528 publicaciones el último mes. Sirve para conseguir pacientes del récord académico.
    id: "fb-pacientes-tratamientos-dentales-gratis",
    nombre: "Pacientes para tratamientos dentales gratis (universidades del Per\xFA)",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/364742402795426",
    tema: "Conseguir pacientes",
    detalle: "Grupo p\xFAblico de Facebook para que los estudiantes de odontolog\xEDa consigan pacientes para su r\xE9cord acad\xE9mico (m\xE1s de 6 600 miembros, 528 publicaciones al mes, desde mayo de 2024).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 12/4/2024, 1 157 miembros; 246 publicaciones el último mes. Su descripción incluye la venta de libros y materiales.
    id: "fb-estudiantes-odontologia-peru-ayuda",
    nombre: "Estudiantes de Odontolog\xEDa Per\xFA (ayuda y venta de libros)",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1571689900289775",
    tema: "Ayuda y venta de material",
    detalle: "Grupo p\xFAblico de Facebook de ayuda a estudiantes de odontolog\xEDa, con venta de libros y materiales (unos 1 200 miembros, 246 publicaciones al mes, desde abril de 2024).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 7/11/2012 (ANTES de 2020), 6 339 miembros; 646 publicaciones el último mes.
    id: "fb-odontologia-estomatologia-peru",
    nombre: "Odontolog\xEDa - Estomatolog\xEDa (Per\xFA)",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/Odontologia.Estomatologia.PERU",
    tema: "Odontolog\xEDa y Estomatolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook para difundir informaci\xF3n de la carrera de odontolog\xEDa y estomatolog\xEDa y sus especialidades (m\xE1s de 6 000 miembros, 646 publicaciones al mes, desde 2012).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 4/9/2012 (ANTES de 2020), 10 790 miembros; 396 publicaciones el último mes. Un resultado de búsqueda mostró el aviso de un curso.
    id: "fb-ciencia-odontologica-peru",
    nombre: "Ciencia Odontol\xF3gica del Per\xFA",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/copdelperu",
    tema: "Odontoestomatolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes, profesionales y pacientes interesados en la odontoestomatolog\xEDa (casi 11 000 miembros, 396 publicaciones al mes, desde 2012). Se ven avisos de cursos.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 25/5/2012 (ANTES de 2020), 43 155 miembros; 2 867 publicaciones el último mes. Un resultado de búsqueda mostró un aviso comercial.
    id: "fb-odontologos-peru",
    nombre: "Odont\xF3logos Per\xFA",
    area: "odontologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/418494371507093",
    tema: "Odontolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook para intercambiar experiencias y conocimientos de odontolog\xEDa (m\xE1s de 43 000 miembros, 2 867 publicaciones al mes, desde 2012). Se ven avisos comerciales.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Nutrición (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 1/8/2017 (ANTES de 2020), 16 173 miembros; 35 publicaciones el último mes; 5 administradores. Los resultados de búsqueda muestran avisos de cursos y diplomados.
    id: "fb-estudiantes-nutricion-nutricionistas-peru",
    nombre: "Estudiantes de Nutrici\xF3n y Nutricionistas Per\xFA",
    area: "nutricion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1532435963497411",
    tema: "Estudiantes de Nutrici\xF3n",
    detalle: "Grupo p\xFAblico de Facebook de estudiantes de nutrici\xF3n y nutricionistas del Per\xFA (m\xE1s de 16 000 miembros, 35 publicaciones al mes, desde 2017). Se ven avisos de cursos y diplomados.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 8/7/2019 (ANTES de 2020), 11 092 miembros; 264 publicaciones el último mes. Los resultados de búsqueda muestran convocatorias de trabajo.
    id: "fb-nutricionistas-peru",
    nombre: "Nutricionistas Per\xFA",
    area: "nutricion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/982020032143934",
    tema: "Nutrici\xF3n",
    detalle: "Grupo p\xFAblico de Facebook de nutricionistas y estudiantes de nutrici\xF3n del Per\xFA (m\xE1s de 11 000 miembros, 264 publicaciones al mes, desde 2019). Se ven convocatorias de trabajo.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/2/2025, 3 300 miembros; 116 publicaciones el último mes. Su descripción habla de materiales y convocatorias de trabajo.
    id: "fb-red-nutricionistas-peru",
    nombre: "Red de Nutricionistas del Per\xFA",
    area: "nutricion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1808989803200955",
    tema: "Red de nutricionistas",
    detalle: "Grupo p\xFAblico de Facebook para intercambiar conocimientos, experiencias, materiales y convocatorias de trabajo de nutrici\xF3n (unos 3 300 miembros, 116 publicaciones al mes, desde febrero de 2025).",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Sociología (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 26/1/2012 (ANTES de 2020), 7 455 miembros; 91 publicaciones el último mes; 1 administrador. Una publicación de un resultado de búsqueda es del Colegio de Sociólogos de Arequipa.
    id: "fb-sociologos-peru",
    nombre: "Soci\xF3logos Per\xFA",
    area: "sociologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/sociologoscaj",
    tema: "Soci\xF3logos",
    detalle: "Grupo p\xFAblico de Facebook para compartir ideas, opiniones y actividades de la sociolog\xEDa (m\xE1s de 7 400 miembros, 91 publicaciones al mes, desde 2012).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/7/2020, 1 098 miembros; 58 publicaciones el último mes. Facebook muestra como administrador a «Colegio de Sociólogos del Perú Región Lima P…».
    id: "fb-comunidad-sociologos-peru",
    nombre: "Comunidad de soci\xF3logos del Per\xFA",
    area: "sociologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/916637635510327",
    tema: "Soci\xF3logos",
    detalle: "Grupo p\xFAblico de Facebook de soci\xF3logos del Per\xFA (unos 1 100 miembros, 58 publicaciones al mes, desde 2020). Aparece con el nombre del Colegio de Soci\xF3logos, Regi\xF3n Lima Provincias; no se confirm\xF3 con su web.",
    administra: "Colegio de Soci\xF3logos, Lima Provincias (sin confirmar)",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/7/2020 (nombre cambiado el 16/6/2024), 1 174 miembros; 60 publicaciones el último mes.
    id: "fb-colegio-sociologos-lima-provincias",
    nombre: "Colegio de Soci\xF3logos del Per\xFA - Regi\xF3n Lima Provincias",
    area: "sociologia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1015473648855672",
    tema: "Colegio de Soci\xF3logos",
    detalle: "Grupo p\xFAblico de Facebook con el nombre del Colegio de Soci\xF3logos del Per\xFA, Regi\xF3n Lima Provincias (unos 1 200 miembros, 60 publicaciones al mes, desde 2020). No se confirm\xF3 con la web del colegio.",
    administra: "Colegio de Soci\xF3logos, Lima Provincias (sin confirmar)",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Ciencias Básicas: Matemática, Física, Química, Biología y Estadística (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones.
  {
    // Público, creado el 7/12/2021, 9 200 miembros; 794 publicaciones el último mes. Su descripción dice «preferiblemente miembros del Perú» y permite promocionar clases los lunes y viernes.
    id: "fb-ayuda-matematicas-peru",
    nombre: "Ayuda y apoyo en Matem\xE1ticas (Per\xFA)",
    area: "ciencias",
    claves: ["matematic", "fisica", "quimica", "estadist"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/652361889442257",
    tema: "Ayuda en ciencias",
    detalle: "Grupo p\xFAblico de Facebook para pedir apoyo en ejercicios de matem\xE1tica, f\xEDsica, qu\xEDmica y estad\xEDstica (unos 9 200 miembros, 794 publicaciones al mes, desde 2021). Se pueden promocionar clases particulares.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 6/2/2021, 85 983 miembros; 1 310 publicaciones el último mes; 1 administrador. Su página NO dice el país: lo cargó el dueño a pedido (13/10/2026).
    id: "fb-estadistica-analisis-datos",
    nombre: "Estad\xEDstica y An\xE1lisis de Datos",
    area: "ciencias",
    claves: ["estadist"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/3802676306442428",
    tema: "Estad\xEDstica y datos",
    detalle: "Grupo p\xFAblico de Facebook para discutir estad\xEDstica y an\xE1lisis de datos (casi 86 000 miembros, 1 310 publicaciones al mes, desde 2021). Es de habla hispana: su p\xE1gina no dice si es de Per\xFA.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 30/12/2012 (ANTES de 2020), 35 500 miembros; 184 publicaciones el último mes; ubicado en Perú; 3 administradores.
    id: "fb-docentes-fisica-peru",
    nombre: "Sociedad Peruana de Docentes de F\xEDsica (SPDF)",
    area: "ciencias",
    claves: ["fisica"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/sopadefideos",
    tema: "Docentes de F\xEDsica",
    detalle: "Grupo p\xFAblico de Facebook de docentes de f\xEDsica y de la comunidad cient\xEDfica peruana (m\xE1s de 35 000 miembros, 184 publicaciones al mes, desde 2012). No se confirm\xF3 que sea de una sociedad oficial.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 24/4/2011 (ANTES de 2020; nombre cambiado el 13/5/2017), 8 855 miembros; 173 publicaciones el último mes.
    id: "fb-biologos-peru",
    nombre: "Bi\xF3logos Per\xFA",
    area: "ciencias",
    claves: ["biolog"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/biologosperu",
    tema: "Biolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de bi\xF3logos y estudiantes de biolog\xEDa del Per\xFA (casi 8 900 miembros, 173 publicaciones al mes, desde 2011). Se vieron avisos de cursos de biolog\xEDa molecular.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Turismo (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 2/10/2012 (ANTES de 2020), 2 950 miembros; 46 publicaciones el último mes; 1 administradora. Abierto a profesionales de cualquier universidad o instituto.
    id: "fb-profesionales-turismo-peru",
    nombre: "Profesionales en Turismo Per\xFA",
    area: "turismo",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/404287619637286",
    tema: "Profesionales de Turismo",
    detalle: "Grupo p\xFAblico de Facebook abierto a profesionales de turismo de cualquier universidad o instituto (casi 3 000 miembros, 46 publicaciones al mes, desde 2012).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 31/3/2020, 2 664 miembros; 140 publicaciones el último mes. Un resultado de búsqueda mostró el aviso de una profesional que ofrece sus servicios.
    id: "fb-comunidad-profesionales-turismo-peru",
    nombre: "Comunidad de Profesionales del Turismo Per\xFA",
    area: "turismo",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/638654120251863",
    tema: "Profesionales de Turismo",
    detalle: "Grupo p\xFAblico de Facebook de profesionales del turismo y la hoteler\xEDa del Per\xFA (unos 2 700 miembros, 140 publicaciones al mes, desde 2020). Se ven avisos de profesionales que buscan trabajo.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Comunicación (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 10/9/2016 (nombre cambiado el 19/7/2023), 8 354 miembros; 200 publicaciones el último mes. Su descripción incluye casting, fotografía, teatro y alquiler de equipos.
    id: "fb-ciencias-comunicacion-lima",
    nombre: "Ciencias de la comunicaci\xF3n Lima-Per\xFA",
    area: "comunicacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/724179387719735",
    tema: "Comunicaci\xF3n y medios",
    detalle: "Grupo p\xFAblico de Facebook de ciencias de la comunicaci\xF3n, casting, fotograf\xEDa, teatro y eventos culturales (m\xE1s de 8 300 miembros, 200 publicaciones al mes, desde 2016). Se ven avisos de alquiler y de trabajo.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 19/7/2017 (nombre cambiado el 13/1/2023), 1 357 miembros; 108 publicaciones el último mes; ubicado en Perú.
    id: "fb-ciencias-comunicacion-marketing",
    nombre: "Ciencias de la Comunicaci\xF3n (Per\xFA)",
    area: "comunicacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/cienciasdelacomunicacionymarketing",
    tema: "Comunicaci\xF3n y marketing",
    detalle: "Grupo p\xFAblico de Facebook para que estudiantes y profesionales de ciencias de la comunicaci\xF3n discutan y aprendan (unos 1 400 miembros, 108 publicaciones al mes, desde 2017). Facebook lo ubica en Per\xFA.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 29/10/2012, 6 346 miembros; 51 publicaciones el último mes; 3 administradores. Dice ser de la Federación de Periodistas del Perú (fundada en 1950); no se confirmó con su web.
    id: "fb-federacion-periodistas-peru",
    nombre: "Federaci\xF3n de Periodistas del Per\xFA",
    area: "comunicacion",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/federaciondeperiodistasdelperu",
    tema: "Periodismo",
    detalle: "Grupo p\xFAblico de Facebook que lleva el nombre de la Federaci\xF3n de Periodistas del Per\xFA, gremio fundado en 1950 (unos 6 300 miembros, 51 publicaciones al mes, desde 2012). No se confirm\xF3 con su web que sea el oficial.",
    administra: "dice ser el gremio de periodistas (sin confirmar)",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Antropología y Arqueología (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 18/5/2020 (nombre cambiado el 19/8/2026), 64 625 miembros; 214 publicaciones el último mes. «Historia, cultura y patrimonio».
    id: "fb-arqueologia-peruana",
    nombre: "Arqueolog\xEDa Peruana",
    area: "antropologia",
    claves: ["arqueolog"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/539378036727339",
    tema: "Arqueolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook sobre historia, cultura y patrimonio del Per\xFA (m\xE1s de 64 000 miembros, 214 publicaciones al mes, desde 2020). Es de aficionados y estudiantes de arqueolog\xEDa.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 15/8/2024, 7 148 miembros; 164 publicaciones el último mes. Facebook muestra como administrador a «Arqueología Peruana».
    id: "fb-arqueologia",
    nombre: "Arqueolog\xEDa (Arqueolog\xEDa Peruana)",
    area: "antropologia",
    claves: ["arqueolog"],
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1067072475016578",
    tema: "Arqueolog\xEDa",
    detalle: "Grupo p\xFAblico de Facebook de arqueolog\xEDa (unos 7 100 miembros, 164 publicaciones al mes, desde 2024). Lo administra la misma cuenta que \xABArqueolog\xEDa Peruana\xBB.",
    administra: "la cuenta \xABArqueolog\xEDa Peruana\xBB",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Gastronomía (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión). Son de cocineros y chefs en general: los de solo estudiantes son chicos o están muertos.
  {
    // Público, creado el 7/9/2013, 105 264 miembros; 707 publicaciones el último mes.
    id: "fb-cocineros-chefs-lima",
    nombre: "Cocineros y Chefs de Lima",
    area: "gastronomia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/cocinerosychefsdelperu",
    tema: "Cocineros y chefs",
    detalle: "Grupo p\xFAblico de Facebook de cocineros y chefs (m\xE1s de 105 000 miembros, 707 publicaciones al mes, desde 2013). Tiene reglamento propio de expulsi\xF3n; puede haber avisos de trabajo.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 12/4/2018, 37 565 miembros; 1 201 publicaciones el último mes; Facebook lo ubica en Perú.
    id: "fb-cocineros-chefs-lima-peru",
    nombre: "Cocineros y Chef de Lima y Per\xFA",
    area: "gastronomia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/421969664930707",
    tema: "T\xE9cnicas y recetas",
    detalle: "Grupo p\xFAblico de Facebook para ver y aprender t\xE9cnicas gastron\xF3micas y recetas (unos 37 600 miembros, 1 201 publicaciones al mes, desde 2018). Facebook lo ubica en Per\xFA.",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 8/12/2016 (nombre cambiado el 30/5/2019), 21 406 miembros; 352 publicaciones el último mes.
    id: "fb-cocineros-chefs-peruanos",
    nombre: "Cocineros y Chefs Peruanos",
    area: "gastronomia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1818425688446694",
    tema: "Cocineros y chefs",
    detalle: "Grupo p\xFAblico de Facebook para que cocineros compartan conocimientos y experiencias (unos 21 400 miembros, 352 publicaciones al mes, desde 2016).",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Farmacia y Bioquímica (13/10/2026): público, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 2/2/2014, 11 514 miembros; 85 publicaciones el último mes; 3 administradores.
    id: "fb-quimicos-farmaceuticos-peru",
    nombre: "Qu\xEDmicos Farmac\xE9uticos Per\xFA",
    area: "farmacia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/quimicosfarmaceuticosperu",
    tema: "Qu\xEDmicos farmac\xE9uticos",
    detalle: "Grupo p\xFAblico de Facebook de qu\xEDmicos farmac\xE9uticos del Per\xFA (m\xE1s de 11 500 miembros, 85 publicaciones al mes, desde 2014). Es de profesionales; los estudiantes tambi\xE9n pueden unirse.",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Obstetricia (13/10/2026): público, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 25/5/2021, 8 393 miembros; 430 publicaciones el último mes; lo administra una cuenta llamada «Obstetra».
    id: "fb-obstetras-peru",
    nombre: "Obstetras del Per\xFA",
    area: "obstetricia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/344711237044397",
    tema: "Obstetras",
    detalle: "Grupo p\xFAblico de Facebook de obstetras del Per\xFA (unos 8 400 miembros, 430 publicaciones al mes, desde 2021). Se ven b\xFAsquedas de trabajo de egresadas.",
    administra: "una cuenta llamada \xABObstetra\xBB",
    revisado: "13 de octubre de 2026"
  },
  // ---------- Historia (13/10/2026): públicos, de 1 000 miembros o más y con 30 publicaciones o más el último mes. No se pudieron ver sus publicaciones (la página principal pide iniciar sesión).
  {
    // Público, creado el 5/12/2019 (ANTES de 2020 por días), 19 500 miembros; 538 publicaciones el último mes.
    id: "fb-historia-del-peru",
    nombre: "Historia del Per\xFA",
    area: "historia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/490312988280040",
    tema: "Historia del Per\xFA",
    detalle: "Grupo p\xFAblico de Facebook para conocer las etapas, hechos y sucesos de la historia del Per\xFA (unos 19 500 miembros, 538 publicaciones al mes, desde diciembre de 2019).",
    revisado: "13 de octubre de 2026"
  },
  {
    // Público, creado el 21/9/2015, 2 623 miembros; 109 publicaciones el último mes; ubicado en Cusco. Un resultado de búsqueda mostró la venta de libros de ciencias sociales.
    id: "fb-comunidad-historiadores-peru",
    nombre: "Comunidad de Historiadores del Per\xFA",
    area: "historia",
    plataforma: "facebook",
    tipo: "grupo",
    url: "https://www.facebook.com/groups/1688064361425878",
    tema: "Historiadores",
    detalle: "Grupo p\xFAblico de Facebook para exponer puntos de vista sobre la realidad nacional e internacional (unos 2 600 miembros, 109 publicaciones al mes, desde 2015, en Cusco). Se ven ventas de libros.",
    revisado: "13 de octubre de 2026"
  }
];
var etiquetaDeArea = (area) => AREAS_COMUNIDADES.find((a) => a.id === area)?.etiqueta ?? area;
function intercalarPorArea(lista) {
  const colas = AREAS_COMUNIDADES.map((a) => lista.filter((c) => c.area === a.id)).filter((q) => q.length > 0);
  const salida2 = [];
  for (let i = 0; colas.some((q) => i < q.length); i++) for (const q of colas) if (i < q.length) salida2.push(q[i]);
  return salida2;
}

// src/data/gruposCurados.ts
var SEDE_TODAS = "todas";
var CARRERA_TODAS = "Todas las carreras";
function etiquetaOrigen(origen) {
  switch (origen) {
    case "uninexo":
      return "Canal de UniNexo";
    case "oficial":
      return "Oficial \xB7 no es de UniNexo";
    case "estudiantil":
      return "Estudiantil \xB7 no oficial";
    case "academia":
      return "Academia \xB7 canal propio \xB7 no es de UniNexo";
    default:
      return "Comunidad abierta \xB7 no es de UniNexo";
  }
}
var CLAVES_AREA = {
  programacion: ["sistemas", "software", "computacion", "informatica", "programacion", "ciberseguridad", "ciencia de datos", "inteligencia artificial"],
  educacion: ["educacion", "pedagog"],
  derecho: ["derecho", "ciencia politica"],
  contabilidad: ["contab", "auditoria", "finanzas"],
  administracion: ["administracion", "negocios"],
  veterinaria: ["veterinari", "zootecn"],
  trabajosocial: ["trabajo social"],
  marketing: ["marketing", "publicidad"],
  psicologia: ["psicolog"],
  enfermeria: ["enfermer"],
  medicina: ["medicina humana"],
  negociosint: ["negocios internacionales", "comercio exterior"],
  economia: ["econom"],
  arquitectura: ["arquitect"],
  odontologia: ["odontolog", "estomatolog"],
  nutricion: ["nutric", "dietet"],
  sociologia: ["sociolog"],
  ciencias: ["matematic", "fisica", "quimica", "biolog", "estadist"],
  turismo: ["turismo", "hoteler"],
  antropologia: ["antropolog", "arqueolog"],
  gastronomia: ["gastronom"],
  farmacia: ["farmac", "bioquim"],
  obstetricia: ["obstetric"],
  historia: ["historia"],
  comunicacion: ["ciencias de la comunicacion", "comunicacion social", "periodis", "audiovisual"],
  ingenieria: ["ingenieria"],
  ambiental: ["ambiental", "agronom", "forestal", "agricola", "agrari", "agropecuari", "zootecn", "veterinari"]
};
var DATOS_CANAL = {
  "unsa-admision": { carrera: CARRERA_TODAS, claves: [], categoria: "cachimbo" },
  "unsm-admision": { carrera: CARRERA_TODAS, claves: [], categoria: "cachimbo" },
  "uni-cepre": { carrera: CARRERA_TODAS, claves: [], categoria: "cachimbo" },
  "uni-oficial-canal": { carrera: CARRERA_TODAS, claves: [], categoria: "general" },
  "unasam-rtv": { carrera: CARRERA_TODAS, claves: [], categoria: "general" },
  "utp-dsc": { carrera: "Programaci\xF3n", claves: CLAVES_AREA.programacion, categoria: "general" },
  "uni-figmm": { carrera: "Ingenier\xEDa Geol\xF3gica, Minera y Metal\xFArgica", claves: ["geolog", "minas", "metalurg"], categoria: "general" },
  "unmsm-educacion-fb": { carrera: "Educaci\xF3n", claves: CLAVES_AREA.educacion, categoria: "general" },
  "unamad-admision-fb": { carrera: CARRERA_TODAS, claves: [], categoria: "cachimbo" },
  "unmsm-derecho-fb": { carrera: "Derecho", claves: CLAVES_AREA.derecho, categoria: "general" },
  "unmsm-estudiantes-derecho-fb": { carrera: "Derecho", claves: CLAVES_AREA.derecho, categoria: "general" },
  "unsa-derecho-fb": { carrera: "Derecho", claves: CLAVES_AREA.derecho, categoria: "general" },
  "unmsm-contables-fb": { carrera: "Contabilidad", claves: CLAVES_AREA.contabilidad, categoria: "general" },
  "unsa-contables-fb": { carrera: "Contabilidad", claves: CLAVES_AREA.contabilidad, categoria: "general" },
  "unt-trabajo-social-fb": { carrera: "Trabajo Social", claves: CLAVES_AREA.trabajosocial, categoria: "general" },
  "uncp-trabajo-social-fb": { carrera: "Trabajo Social", claves: CLAVES_AREA.trabajosocial, categoria: "general" },
  "unmsm-odontologia-fb": { carrera: "Odontolog\xEDa", claves: CLAVES_AREA.odontologia, categoria: "general" },
  "usmp-odontologia-fb": { carrera: "Odontolog\xEDa", claves: CLAVES_AREA.odontologia, categoria: "general" },
  "upch-estomatologia-fb": { carrera: "Odontolog\xEDa", claves: CLAVES_AREA.odontologia, categoria: "general" },
  "uncp-antropologia-fb": { carrera: "Antropolog\xEDa", claves: ["antropolog"], categoria: "general" },
  "unsaac-arqueologia-fb": { carrera: "Arqueolog\xEDa", claves: ["arqueolog"], categoria: "general" },
  "unmsm-historia-fb": { carrera: "Historia", claves: CLAVES_AREA.historia, categoria: "general" },
  "unfv-historia-fb": { carrera: "Historia", claves: CLAVES_AREA.historia, categoria: "general" },
  "pucp-historia-fb": { carrera: "Historia", claves: CLAVES_AREA.historia, categoria: "general" },
  "unsaac-obstetricia-fb": { carrera: "Obstetricia", claves: CLAVES_AREA.obstetricia, categoria: "general" },
  "unsaac-comunicacion-fb": { carrera: "Ciencias de la Comunicaci\xF3n", claves: CLAVES_AREA.comunicacion, categoria: "general" },
  "unmsm-quimica-fb": { carrera: "Qu\xEDmica", claves: ["quimic"], categoria: "general" },
  "upc-arquitectura-fb": { carrera: "Arquitectura", claves: CLAVES_AREA.arquitectura, categoria: "general" },
  "pucp-economia-fb": { carrera: "Econom\xEDa", claves: CLAVES_AREA.economia, categoria: "general" },
  "unmsm-medicina-fb": { carrera: "Medicina", claves: CLAVES_AREA.medicina, categoria: "general" },
  "ucv-medicina-fb": { carrera: "Medicina", claves: CLAVES_AREA.medicina, categoria: "general" },
  "unjfsc-medicina-fb": { carrera: "Medicina", claves: CLAVES_AREA.medicina, categoria: "general" },
  "unsa-enfermeria-fb": { carrera: "Enfermer\xEDa", claves: CLAVES_AREA.enfermeria, categoria: "general" },
  "urp-medicina-veterinaria-fb": { carrera: "Veterinaria", claves: CLAVES_AREA.veterinaria, categoria: "general" }
};
var ORIGEN_CANAL = { universidad: "oficial", estudiantil: "estudiantil", abierta: "abierta" };
function desdeCanalUniversidad(c) {
  const datos = DATOS_CANAL[c.id] ?? { carrera: CARRERA_TODAS, claves: [], categoria: "general" };
  return {
    id: `cur-${c.id}`,
    universityId: c.universityId,
    sedeId: SEDE_TODAS,
    carrera: datos.carrera,
    title: c.nombre,
    platform: c.plataforma,
    category: datos.categoria,
    link: c.url,
    description: c.detalle,
    carreraClaves: datos.claves,
    origen: ORIGEN_CANAL[c.origen],
    tipo: tipoDeCanal(c.url, c.plataforma),
    administra: c.administra ?? (c.origen === "universidad" ? "la universidad" : "estudiantes (no es oficial)"),
    revisado: c.revisado ?? FECHA_REVISION_CANALES
  };
}
function desdeCanalEstado(c) {
  return {
    id: `cur-${c.id}`,
    universityId: UNI_GENERAL_ID,
    sedeId: SEDE_TODAS,
    carrera: CARRERA_TODAS,
    title: c.nombre,
    platform: "whatsapp",
    category: "general",
    link: c.url,
    description: c.detalle,
    carreraClaves: [],
    origen: "oficial",
    tipo: "canal",
    administra: c.administra,
    tema: c.tema,
    revisado: c.revisado
  };
}
function desdeCanalAcademia(c) {
  return {
    id: `cur-${c.id}`,
    universityId: UNI_GENERAL_ID,
    sedeId: SEDE_TODAS,
    carrera: CARRERA_TODAS,
    title: c.nombre,
    platform: "whatsapp",
    category: "cachimbo",
    link: c.url,
    description: c.detalle,
    carreraClaves: [],
    origen: "academia",
    tipo: "canal",
    administra: "la academia",
    tema: "Preuniversitaria",
    revisado: c.revisado
  };
}
function desdeComunidad(c) {
  return {
    id: `cur-${c.id}`,
    universityId: UNI_GENERAL_ID,
    sedeId: SEDE_TODAS,
    carrera: etiquetaDeArea(c.area),
    title: c.nombre,
    platform: c.plataforma,
    category: c.area === "programacion" ? "curso" : "general",
    link: c.url,
    description: c.detalle,
    carreraClaves: c.claves ?? CLAVES_AREA[c.area],
    origen: c.oficial ? "oficial" : "abierta",
    tipo: c.tipo,
    administra: c.administra ?? "sus propios creadores",
    tema: c.tema,
    revisado: c.revisado ?? FECHA_REVISION_COMUNIDADES
  };
}
var GRUPOS_CURADOS = [
  ...CANALES_UNIVERSIDADES.map(desdeCanalUniversidad),
  ...CANALES_ESTADO.map(desdeCanalEstado),
  ...CANALES_ACADEMIAS.map(desdeCanalAcademia),
  ...intercalarPorArea(COMUNIDADES_POR_CARRERA).map(desdeComunidad)
];

// src/data/redesUniversidades.ts
var NOMBRE_RED = {
  facebook: "Facebook",
  instagram: "Instagram",
  tiktok: "TikTok",
  x: "X",
  youtube: "YouTube"
};
var REDES_UNIVERSIDADES = [
  {
    universityId: "unmsm",
    fuente: "https://www.unmsm.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/1551UNMSM" },
      { red: "instagram", url: "https://www.instagram.com/unmsm_/" },
      { red: "tiktok", url: "https://www.tiktok.com/@unmsm" },
      { red: "youtube", url: "https://www.youtube.com/user/RTVSanMarcos", de: "RTV San Marcos" }
    ]
  },
  {
    universityId: "uni",
    fuente: "https://www.gob.pe/institucion/uni/contacto-y-numeros-de-emergencias",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/UNIoficial.pe" },
      { red: "instagram", url: "https://www.instagram.com/uni_oficial/" },
      { red: "x", url: "https://x.com/UNIoficial" }
    ]
  },
  {
    universityId: "unfv",
    fuente: "https://www.unfv.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/UNFV.EDU" },
      { red: "instagram", url: "https://www.instagram.com/unfvoficial/" },
      { red: "tiktok", url: "https://www.tiktok.com/@unfv" },
      { red: "x", url: "https://x.com/UNFVoficial" },
      { red: "youtube", url: "https://www.youtube.com/user/PrensaUNFV", de: "Prensa UNFV" }
    ]
  },
  {
    universityId: "unt",
    fuente: "https://www.unitru.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/untlaunicaoficial" },
      { red: "facebook", url: "https://www.facebook.com/Direcci%C3%B3n-de-Bienestar-Universitario-UNT-100925675091841/", de: "Bienestar Universitario" },
      { red: "youtube", url: "https://www.youtube.com/@universidadnacionaldetrujillo" }
    ]
  },
  {
    universityId: "unsa",
    fuente: "https://www.unsa.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/PaginaOficialUNSA" },
      { red: "facebook", url: "https://www.facebook.com/subdireccionbienestaruniversitario", de: "Bienestar Universitario" },
      { red: "instagram", url: "https://www.instagram.com/unsa.bienestar", de: "Bienestar Universitario" }
    ]
  },
  {
    universityId: "unsaac",
    fuente: "https://www.unsaac.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/UNSAACPag.Oficial" },
      { red: "instagram", url: "https://www.instagram.com/unsaac_oficial/" },
      { red: "youtube", url: "https://www.youtube.com/@VideosInstitucionalesUNSAAC" }
    ]
  },
  {
    universityId: "uncp",
    fuente: "https://uncp.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/UNCPoficial" },
      { red: "x", url: "https://x.com/_UNCP_oficial" },
      { red: "tiktok", url: "https://www.tiktok.com/@uncp.oficial" },
      { red: "youtube", url: "https://www.youtube.com/user/UNCPvideos" }
    ]
  },
  {
    universityId: "unamad",
    fuente: "https://portal.unamad.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/unamad.oficial/" },
      { red: "instagram", url: "https://www.instagram.com/unamad_oficial/" },
      { red: "youtube", url: "https://www.youtube.com/channel/UCUNGgRNunGECIxEd_-qv_oA" }
    ]
  },
  {
    universityId: "une",
    fuente: "https://www.une.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/UNEoficialPeru/" },
      { red: "instagram", url: "https://www.instagram.com/uneoficialperu/" },
      { red: "instagram", url: "https://www.instagram.com/une.imagen/", de: "Imagen" },
      { red: "tiktok", url: "https://www.tiktok.com/@uneoficialperu" },
      { red: "youtube", url: "https://www.youtube.com/channel/UC3GS9EVP_tSTpiM6FI7XwRw" }
    ]
  },
  {
    universityId: "unheval",
    fuente: "https://unheval.edu.pe/portal/",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/unheval.edu.pe" },
      { red: "instagram", url: "https://www.instagram.com/unheval.edu.pe/" },
      { red: "tiktok", url: "https://www.tiktok.com/@unheval.edu.pe" },
      { red: "x", url: "https://x.com/unheval_pe" },
      { red: "youtube", url: "https://www.youtube.com/@unhevaloficial" }
    ]
  },
  {
    universityId: "unasam",
    fuente: "https://www.unasam.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/unasam.edu.pe" },
      { red: "instagram", url: "https://www.instagram.com/unasam_oficial/" },
      { red: "youtube", url: "https://www.youtube.com/channel/UCHUxOdDI4zrMgghSpTDxttw" }
    ]
  },
  {
    universityId: "unca",
    fuente: "https://unca.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/universidadnacionalciroalegria" },
      { red: "instagram", url: "https://www.instagram.com/universidadnacionalciroalegria" },
      { red: "youtube", url: "https://www.youtube.com/@UNCiroAlegria" }
    ]
  },
  {
    universityId: "unu",
    fuente: "https://www.unu.edu.pe/portal/",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/udeucayali" },
      { red: "instagram", url: "https://www.instagram.com/unucayali_oficial/" },
      { red: "tiktok", url: "https://www.tiktok.com/@unu_oficial" },
      { red: "youtube", url: "https://www.youtube.com/@universidadnacionaldeucayali" }
    ]
  },
  {
    universityId: "unh",
    fuente: "https://www.unh.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/universidadunh" },
      { red: "youtube", url: "https://www.youtube.com/channel/UCU1xRWArgbVQR9qUM7j6J5Q" }
    ]
  },
  {
    universityId: "unsm",
    fuente: "https://unsm.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/unsmperu/" },
      { red: "x", url: "https://x.com/unsmperu" },
      { red: "youtube", url: "https://www.youtube.com/channel/UCJY5_-Kj4K3soc0LtEC4sLA" }
    ]
  },
  {
    universityId: "unia",
    fuente: "https://unia.edu.pe",
    cuentas: [
      { red: "facebook", url: "https://www.facebook.com/unia.edu.pe" },
      { red: "instagram", url: "https://www.instagram.com/unia_intercultural/" }
    ]
  }
];
var redesDe = (universityId) => REDES_UNIVERSIDADES.find((r) => r.universityId === universityId);

// src/data/guiaCachimbo.ts
var WEB_OFICIAL_UNIVERSIDAD = {
  unmsm: "https://unmsm.edu.pe",
  uni: "https://www.uni.edu.pe",
  unalm: "https://www.lamolina.edu.pe",
  unfv: "https://www.unfv.edu.pe",
  unac: "https://www.unac.edu.pe",
  unt: "https://www.unitru.edu.pe",
  unprg: "https://www.unprg.edu.pe",
  uncp: "https://www.uncp.edu.pe",
  unica: "https://www.unica.edu.pe",
  unsa: "https://www.unsa.edu.pe",
  unsaac: "https://www.unsaac.edu.pe",
  unamad: "https://www.unamad.edu.pe",
  pucp: "https://www.pucp.edu.pe",
  ulima: "https://www.ulima.edu.pe",
  up: "https://www.up.edu.pe",
  upch: "https://cayetano.edu.pe",
  upc: "https://www.upc.edu.pe",
  usil: "https://www.usil.edu.pe",
  usmp: "https://www.usmp.edu.pe",
  utp: "https://www.utp.edu.pe",
  ucv: "https://www.ucv.edu.pe"
};

// src/utils/paginaUniversidad.ts
var ALIAS_ACADEMIA = {
  "san marcos": "unmsm",
  villarreal: "unfv",
  "u. del callao": "unac",
  untumbes: "untumbes",
  "agraria": "unalm",
  "agraria la molina": "unalm",
  "u. de lima": "ulima",
  ulima: "ulima",
  "u. del pacifico": "up",
  "cientifica del sur": "ucsur",
  "una puno": "unap-puno"
};
var sinTildes = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
function universidadesDeAcademia(a) {
  const ids = /* @__PURE__ */ new Set();
  for (const texto of a.universidades || []) {
    const t = sinTildes(texto);
    if (t === "unap") ids.add(sinTildes(a.region || "") === "loreto" ? "unap-loreto" : "unap-puno");
    else if (ALIAS_ACADEMIA[t]) ids.add(ALIAS_ACADEMIA[t]);
    else {
      const u = PERU_UNIVERSITIES.find((x) => sinTildes(x.acronym) === t);
      if (u) ids.add(u.id);
    }
  }
  return [...ids];
}
function armarPaginaUniversidad(uniId, ext) {
  const uni = PERU_UNIVERSITIES.find((u) => u.id === uniId);
  if (!uni) return null;
  const redes = redesDe(uniId);
  const mats = ext.materiales;
  return {
    uni,
    grupos: GRUPOS_CURADOS.filter((g) => g.universityId === uniId),
    redes: redes ? redes.cuentas.map((c) => ({ red: NOMBRE_RED[c.red], url: c.url, de: c.de })) : [],
    webOficial: WEB_OFICIAL_UNIVERSIDAD[uniId],
    examenes: mats.filter((m) => m.type === "examen"),
    otrosMateriales: mats.filter((m) => m.type !== "examen"),
    academias: ext.academias.filter((a) => universidadesDeAcademia(a).includes(uniId)),
    docentes: ext.docentes,
    ciudades: [...new Set(uni.sedes.map((s) => s.city).filter(Boolean))]
  };
}
function bloquesConDatos(p) {
  return [p.grupos.length, p.redes.length, p.examenes.length + p.otrosMateriales.length, p.academias.length, p.docentes.length].filter((n) => n > 0).length;
}
function tienePaginaPropia(p) {
  return (p.grupos.length > 0 || p.redes.length > 0) && bloquesConDatos(p) >= 3;
}
function preguntasUniversidad(p) {
  const s = p.uni.acronym;
  const lista = [];
  if (p.grupos.length) {
    const oficiales = p.grupos.filter((g) => g.origen === "oficial").length;
    lista.push({
      pregunta: `\xBFD\xF3nde encuentro los grupos de WhatsApp, Telegram o Facebook de la ${s}?`,
      respuesta: `En UniNexo Per\xFA hay ${p.grupos.length} ${p.grupos.length === 1 ? "grupo o canal" : "grupos y canales"} de la ${s}${oficiales ? `, ${oficiales} de ellos oficiales de la universidad` : ""}. Cada uno dice qui\xE9n lo administra y si es oficial o no. Ning\xFAn grupo real te pide dinero ni el c\xF3digo que llega por SMS.`
    });
  }
  if (p.examenes.length) {
    lista.push({
      pregunta: `\xBFD\xF3nde descargo ex\xE1menes de admisi\xF3n de la ${s}?`,
      respuesta: `UniNexo Per\xFA tiene ${p.examenes.length} ${p.examenes.length === 1 ? "examen" : "ex\xE1menes"} de admisi\xF3n de la ${s} con su fuente: ${p.examenes.slice(0, 3).map((m) => m.title).join("; ")}.`
    });
  }
  if (p.academias.length) {
    lista.push({
      pregunta: `\xBFQu\xE9 academias preparan para la ${s}?`,
      respuesta: `${p.academias.slice(0, 6).map((a) => `${a.nombre}${a.region ? ` (${a.region})` : ""}`).join(", ")}${p.academias.length > 6 ? " y otras" : ""}. Sus datos salen de su web oficial.`
    });
  }
  if (p.redes.length) {
    lista.push({
      pregunta: `\xBFCu\xE1les son las redes oficiales de la ${s}?`,
      respuesta: `${[...new Set(p.redes.map((r) => r.red))].join(", ")}, tomadas de la web oficial de la universidad.`
    });
  }
  return lista;
}

// src/utils/entradaBlogUniversidad.ts
var SITIO = "https://uninexo.link";
var esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
var RED = { whatsapp: ["\u{1F7E2}", "WhatsApp"], telegram: ["\u2708\uFE0F", "Telegram"], facebook: ["\u{1F535}", "Facebook"], discord: ["\u{1F3AE}", "Discord"] };
var ORDEN_RED = { whatsapp: 0, telegram: 1, discord: 2, facebook: 3 };
function cortar(s, max = 150) {
  const t = s.replace(/\s+/g, " ").trim();
  if (t.length <= max) return t;
  const c = t.slice(0, max);
  return c.slice(0, c.lastIndexOf(" ")).replace(/[,;:(\s]+$/, "") + "\u2026";
}
function miembrosDe(g) {
  const m = g.description.match(/(\d{1,3}(?:[  .]\d{3})+|\d+)\s+(?:miembros|seguidores)/);
  return m ? Number(m[1].replace(/[^\d]/g, "")) : 0;
}
function sirveParaBlog(p) {
  return tienePaginaPropia(p) && p.grupos.length >= 2;
}
var ordenarGrupos = (gs) => [...gs].sort((a, b) => (ORDEN_RED[a.platform] ?? 9) - (ORDEN_RED[b.platform] ?? 9) || miembrosDe(b) - miembrosDe(a));
function introduccion(p) {
  const s = p.uni.acronym;
  const oficiales = p.grupos.filter((g) => g.origen === "oficial");
  const fb = p.grupos.filter((g) => g.platform === "facebook");
  const mayor = [...p.grupos].sort((a, b) => miembrosDe(b) - miembrosDe(a))[0];
  const partes = [];
  partes.push(`La <b>${esc(p.uni.name)}</b> (${esc(s)}) es una universidad ${p.uni.type === "publica" ? "p\xFAblica" : "privada"}${p.ciudades.length ? ` con sede en ${esc(p.ciudades.slice(0, 3).join(", "))}` : ""}.`);
  if (oficiales.length) {
    partes.push(`Tiene ${oficiales.length === 1 ? "un canal oficial" : `${oficiales.length} canales oficiales`} (${esc(oficiales.map((g) => g.title).join(", "))}), la forma m\xE1s segura de enterarte de sus avisos.`);
  }
  if (fb.length) {
    partes.push(`Sus estudiantes se organizan sobre todo en ${fb.length === 1 ? "un grupo" : `${fb.length} grupos`} de Facebook${mayor && miembrosDe(mayor) ? `; el m\xE1s grande, \xAB${esc(mayor.title)}\xBB, re\xFAne a unas ${miembrosDe(mayor).toLocaleString("es-PE")} personas` : ""}.`);
  }
  const extra = [];
  if (p.examenes.length) extra.push(`${p.examenes.length} ${p.examenes.length === 1 ? "examen" : "ex\xE1menes"} de admisi\xF3n`);
  if (p.academias.length) extra.push(`${p.academias.length} ${p.academias.length === 1 ? "academia" : "academias"} que preparan para ella`);
  if (p.docentes.length) extra.push(`${p.docentes.length} ${p.docentes.length === 1 ? "docente" : "docentes"} con reconocimiento p\xFAblico`);
  if (extra.length) partes.push(`En UniNexo tambi\xE9n encontrar\xE1s ${extra.join(", ").replace(/, ([^,]*)$/, " y $1")}.`);
  return partes.join(" ");
}
function huellaPagina(p) {
  const base = [
    p.grupos.map((g) => g.id).sort().join(","),
    p.academias.map((a) => a.id).sort().join(","),
    p.examenes.map((m) => m.id).sort().join(","),
    p.docentes.map((d) => d.id).sort().join(","),
    p.redes.map((r) => r.url).sort().join(",")
  ].join("|");
  let h = 0;
  for (let i = 0; i < base.length; i++) h = h * 31 + base.charCodeAt(i) | 0;
  return (h >>> 0).toString(36);
}
function armarEntradaUniversidad(p, hoy2) {
  if (!sirveParaBlog(p)) return null;
  const { uni } = p;
  const s = esc(uni.acronym);
  const pag = `${SITIO}/universidad/${uni.id}`;
  const grupos = ordenarGrupos(p.grupos);
  const redesDeGrupos = [...new Set(grupos.map((g) => g.platform))];
  const cuenta = (pl) => grupos.filter((g) => g.platform === pl).length;
  const nombresRed = redesDeGrupos.map((r) => RED[r]?.[1] || r);
  const titulo = `Grupos de ${nombresRed.join(", ").replace(/, ([^,]*)$/, " y $1")} de la ${uni.acronym} (${uni.name}) 2026`;
  const descripcion = cortar(`${grupos.length} grupos y canales de la ${uni.acronym}: ${nombresRed.join(", ")}, con qui\xE9n los administra${p.examenes.length ? ", ex\xE1menes de admisi\xF3n" : ""}${p.academias.length ? " y academias" : ""}. \xDAnete desde UniNexo Per\xFA.`, 158);
  const preguntas = preguntasUniversidad(p);
  preguntas.push(
    { pregunta: `\xBFLos grupos de la ${uni.acronym} son oficiales?`, respuesta: `Solo los que tienen la etiqueta \xABOficial\xBB. La mayor\xEDa son grupos de estudiantes; en UniNexo cada uno dice qui\xE9n lo administra.` },
    { pregunta: "\xBFCuesta algo unirse?", respuesta: "No. Ning\xFAn grupo real cobra por entrar ni pide el c\xF3digo que te llega por SMS. Si te lo piden, es estafa." }
  );
  const tarjeta = (g) => {
    const [em, red] = RED[g.platform] || ["\u{1F4AC}", g.platform];
    const tipo = { canal: "Canal", grupo: "Grupo", servidor: "Servidor" }[g.tipo] || "Grupo";
    const oficial = g.origen === "oficial";
    return `  <a class="unx-g ${g.platform}" data-p="${g.platform}" href="${pag}" target="_blank"><span class="cab"><span class="red">${em} ${tipo} de ${red}</span><span class="ori ${oficial ? "of" : "no"}">${esc(etiquetaOrigen(g.origen).split("\xB7")[0].trim())}</span></span><span class="tit">${esc(g.title)}</span><span class="des">${esc(cortar(g.description))}</span><span class="adm">Administra: ${esc(cortar(g.administra, 70))}</span><span class="ir">Unirme desde UniNexo \u2192</span></a>`;
  };
  const filtros = redesDeGrupos.length > 1 ? `<div class="unx-redes">
    <button class="unx-red activo" type="button" data-p="">\u2728 Todos (${grupos.length})</button>
${redesDeGrupos.map((r) => `    <button class="unx-red" type="button" data-p="${r}">${RED[r][0]} ${RED[r][1]} (${cuenta(r)})</button>`).join("\n")}
  </div>` : "";
  let cuerpo = `<div class="unx-hero">
  <div class="marca"><img src="${SITIO}/icons/icono-192.png" alt="UniNexo Per\xFA"> UniNexo <b>Per\xFA</b> <span class="unx-vivo"><i></i> ${s}</span></div>
  <h2 class="titulo">\u{1F4AC} Grupos y canales de la ${s}</h2>
  <p class="lead">${introduccion(p)}</p>
  <div class="unx-cifras">
    <div class="unx-cifra"><b>${grupos.length}</b><span>grupos y canales</span></div>
${redesDeGrupos.map((r) => `    <div class="unx-cifra"><b>${cuenta(r)}</b><span>de ${RED[r][1]}</span></div>`).join("\n")}
  </div>
  <a class="unx-boton" href="${pag}" target="_blank">Ver todo de la ${s} en UniNexo \u2192</a>
</div>

<p class="unx-nota">\u2139\uFE0F Datos de UniNexo Per\xFA al ${hoy2}. Al tocar un grupo vas a la p\xE1gina de la ${s} en UniNexo, donde te unes con un aviso de seguridad. UniNexo no pertenece a la universidad.</p>

<h2>\u{1F465} Grupos y canales de la ${s}</h2>
<div class="unx-dir">
  ${filtros}
  <div class="unx-grupos">
${grupos.map(tarjeta).join("\n")}
  </div>
</div>

<div class="unx-franja"><span>\u{1F465} \xBFFalta el grupo de tu sal\xF3n de la ${s}? Publ\xEDcalo gratis en UniNexo</span><a href="${SITIO}/" target="_blank">Publicar mi grupo \u2192</a></div>

`;
  if (p.redes.length) {
    cuerpo += `
<h2>\u{1F4E3} Redes oficiales de la ${s}</h2>
<p>Tomadas de la web oficial de la universidad:</p>
<ul>${p.redes.map((r) => `<li><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.red)}${r.de ? ` (${esc(r.de)})` : ""}</a></li>`).join("")}</ul>
`;
  }
  if (p.examenes.length) {
    cuerpo += `
<h2>\u{1F4DD} Ex\xE1menes de admisi\xF3n de la ${s}</h2>
<ul>${p.examenes.slice(0, 8).map((m) => `<li><a href="${SITIO}/?tab=materiales&amp;uni=${uni.id}" target="_blank">${esc(m.title)}</a></li>`).join("")}</ul>
<p><a href="${SITIO}/examenes" target="_blank">Ver todos los ex\xE1menes de admisi\xF3n en UniNexo \u2192</a></p>
`;
  }
  if (p.academias.length) {
    cuerpo += `
<h2>\u{1F3EB} Academias que preparan para la ${s}</h2>
<ul>${p.academias.slice(0, 10).map((a) => `<li><a href="${SITIO}/academia" target="_blank">${esc(a.nombre)}</a>${a.region ? ` \xB7 ${esc(a.region)}` : ""}</li>`).join("")}</ul>
`;
  }
  if (p.docentes.length) {
    cuerpo += `
<h2>\u{1F52C} Docentes de la ${s} con reconocimiento p\xFAblico</h2>
<ul>${p.docentes.slice(0, 5).map((d) => `<li><b>${esc(d.name)}</b>${d.reconocimiento ? ` \u2014 ${esc(cortar(d.reconocimiento, 110))}` : ""}</li>`).join("")}</ul>
<p class="unx-nota">Es un reconocimiento a su investigaci\xF3n, no una evaluaci\xF3n de sus clases.</p>
`;
  }
  if (p.webOficial) cuerpo += `
<p>\u{1F310} Web oficial de la ${s}: <a href="${esc(p.webOficial)}" target="_blank" rel="noopener">${esc(p.webOficial)}</a></p>
`;
  cuerpo += `
<p class="unx-alerta">\u{1F6E1}\uFE0F Ning\xFAn grupo real te cobra por entrar ni te vende \xABvacantes\xBB o \xABex\xE1menes\xBB. Nunca compartas tu DNI, claves ni el c\xF3digo que te llega por SMS.</p>

<div class="unx-cta">
  <h3>\u{1F3AF} Todo de la ${s} en un solo lugar</h3>
  <p>Grupos, redes oficiales, ex\xE1menes, academias y docentes de la ${esc(uni.name)}. Gratis en UniNexo Per\xFA.</p>
  <div class="botones">
    <a class="prin" href="${pag}" target="_blank">P\xE1gina de la ${s}</a>
    <a href="${SITIO}/" target="_blank">Buscar grupos</a>
    <a href="${SITIO}/examenes" target="_blank">Ex\xE1menes</a>
    <a href="${SITIO}/preu/test-intereses" target="_blank">Test de carrera</a>
  </div>
</div>

<h2>\u2753 Preguntas frecuentes</h2>
<div class="unx-faq">
${preguntas.map((q) => `  <div class="p"><button class="q" type="button">${esc(q.pregunta)}<span class="signo">+</span></button>
    <div class="r">${esc(q.respuesta)}</div></div>`).join("\n")}
</div>

<p class="unx-pie">UniNexo Per\xFA es una plataforma independiente y gratuita. No pertenece a la ${esc(uni.name)} ni administra los grupos que lista. \xBFTe sirvi\xF3? Comp\xE1rtelo con tu promo \u{1F49C} \xB7 <a href="${SITIO}" target="_blank">uninexo.link</a></p>
`;
  const html = `${ESTILO}
<div class="unx" id="unx-post">

${cuerpo}
</div>

${SCRIPT}`;
  return {
    uniId: uni.id,
    titulo,
    slug: `grupos-whatsapp-facebook-${uni.id}-uninexo-peru`,
    etiquetas: [uni.acronym, "Grupos de WhatsApp", "Grupos de Facebook", "Universidades del Per\xFA", ...p.ciudades[0] ? [p.ciudades[0]] : [], "UniNexo Per\xFA"],
    descripcion,
    html,
    huella: huellaPagina(p)
  };
}
var ESTILO = `<style>
.unx{font-family:'Segoe UI',Roboto,Arial,sans-serif;color:#1e1b4b;font-size:17px;line-height:1.75}
.unx *{box-sizing:border-box}
.unx a{color:#6d28d9;font-weight:600}
.unx p{margin:0 0 14px}
.unx-hero{background:linear-gradient(135deg,#7c3aed,#4c1d95,#1e1036,#16a34a);background-size:300% 300%;animation:unxFondo 12s ease infinite;color:#fff;border-radius:24px;padding:30px 26px;margin:0 0 26px;position:relative;overflow:hidden}
@keyframes unxFondo{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.unx-hero .marca{display:flex;align-items:center;gap:10px;font-weight:800;font-size:15px}
.unx-hero .marca img{width:36px;height:36px;border-radius:10px;margin:0}
.unx-hero .marca b{color:#fbbf24}
.unx-vivo{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);border-radius:999px;padding:3px 10px;font-size:12px;font-weight:800;letter-spacing:.5px}
.unx-vivo i{width:8px;height:8px;border-radius:50%;background:#4ade80;animation:unxLatido 1.6s infinite}
@keyframes unxLatido{0%{box-shadow:0 0 0 0 rgba(74,222,128,.7)}70%{box-shadow:0 0 0 10px rgba(74,222,128,0)}100%{box-shadow:0 0 0 0 rgba(74,222,128,0)}}
.unx-hero .titulo{border:0;padding:0;margin:18px 0 8px;color:#fff;font-size:30px;line-height:1.2}
.unx-hero .lead{font-size:17px;margin:0;color:#ede9fe}
.unx-cifras{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-top:18px}
.unx-cifra{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:12px;text-align:center}
.unx-cifra b{display:block;font-size:28px;color:#fbbf24;line-height:1.1}
.unx-cifra span{font-size:13px;color:#ede9fe}
.unx-boton{display:inline-block;background:#fbbf24;color:#3b0764!important;font-weight:800;text-decoration:none;border-radius:14px;padding:13px 20px;margin-top:18px;transition:transform .2s}
.unx-boton:hover{transform:translateY(-3px)}
.unx h2{font-size:24px;color:#4c1d95;margin:36px 0 14px;padding-left:14px;border-left:5px solid #fbbf24;line-height:1.3}
.unx ul{padding-left:22px}.unx li{margin:6px 0}
.unx-nota{background:#f5f3ff;border:1px solid #ddd6fe;border-radius:14px;padding:12px 16px;font-size:15px;color:#4c1d95}
.unx-alerta{background:#fef2f2;border:1px solid #fecaca;border-radius:14px;padding:14px 18px}
.unx-franja{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;background:linear-gradient(90deg,#22c55e,#16a34a);color:#fff;border-radius:18px;padding:16px 20px;margin:24px 0;font-weight:800}
.unx-franja a{background:#fff;color:#166534!important;text-decoration:none;border-radius:12px;padding:10px 16px;white-space:nowrap}
.unx-dir{background:#fff;border:2px solid #7c3aed;border-radius:22px;padding:18px}
.unx-redes{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.unx-red{border:2px solid #ede9fe;background:#fff;border-radius:999px;padding:7px 14px;font:inherit;font-size:15px;font-weight:800;color:#4c1d95;cursor:pointer}
.unx-red.activo{background:#7c3aed;border-color:#7c3aed;color:#fff}
.unx-grupos{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.unx-g{display:flex;flex-direction:column;text-decoration:none;background:#fff;border:1px solid #ede9fe;border-left:5px solid #7c3aed;border-radius:16px;padding:14px;transition:transform .2s,box-shadow .2s}
.unx-g:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(124,58,237,.16)}
.unx-g.whatsapp{border-left-color:#16a34a}.unx-g.facebook{border-left-color:#1877f2}.unx-g.telegram{border-left-color:#0ea5e9}
.unx-g .cab{display:flex;justify-content:space-between;gap:6px;align-items:center}
.unx-g .red{font-size:12px;font-weight:800;color:#374151}
.unx-g .ori{font-size:11px;font-weight:800;border-radius:8px;padding:1px 8px}
.unx-g .ori.of{background:#dcfce7;color:#166534}.unx-g .ori.no{background:#f3f4f6;color:#4b5563}
.unx-g .tit{color:#1e1b4b;font-weight:800;margin:8px 0 4px;line-height:1.3}
.unx-g .des{color:#6b7280;font-size:13px;line-height:1.45;flex:1;font-weight:400}
.unx-g .adm{color:#4c1d95;font-size:12px;margin-top:6px;font-weight:600}
.unx-g .ir{margin-top:10px;color:#6d28d9;font-size:14px;font-weight:800}
.unx-g.oculta{display:none}
.unx-cta{background:linear-gradient(135deg,#1e1036,#4c1d95);color:#fff;border-radius:24px;padding:26px 22px;margin:34px 0}
.unx-cta h3{margin:0 0 6px;font-size:23px;color:#fff}.unx-cta p{color:#ede9fe;margin:0 0 14px}
.unx-cta .botones a{display:inline-block;background:#fff;color:#4c1d95;text-decoration:none;border-radius:12px;padding:10px 14px;margin:4px 6px 4px 0;font-size:15px}
.unx-cta .botones a.prin{background:#fbbf24;color:#3b0764;font-weight:800}
.unx-faq .p{border:1px solid #ede9fe;border-radius:14px;margin:10px 0;background:#fff;overflow:hidden}
.unx-faq .p.abierta{border-color:#7c3aed;box-shadow:0 8px 22px rgba(124,58,237,.14)}
.unx-faq .q{display:flex;width:100%;align-items:center;justify-content:space-between;gap:12px;background:none;border:0;padding:14px 16px;font:inherit;font-weight:700;color:#4c1d95;text-align:left;cursor:pointer}
.unx-faq .signo{flex:none;width:28px;height:28px;border-radius:50%;background:#ede9fe;color:#6d28d9;font-weight:800;display:flex;align-items:center;justify-content:center;transition:transform .3s}
.unx-faq .p.abierta .signo{transform:rotate(45deg);background:#7c3aed;color:#fff}
.unx-faq .r{padding:0 16px 14px;color:#374151}
.unx-js .unx-faq .r{max-height:0;padding-bottom:0;opacity:0;overflow:hidden;transition:max-height .35s,opacity .3s,padding .3s}
.unx-js .unx-faq .p.abierta .r{max-height:500px;opacity:1;padding-bottom:14px}
.unx-pie{font-size:14px;color:#6b7280;border-top:1px solid #e5e7eb;padding-top:14px;margin-top:30px}
@media (prefers-reduced-motion:reduce){.unx *{animation:none!important;transition:none!important}}
</style>`;
var SCRIPT = `<script>
(function () {
  var post = document.getElementById('unx-post');
  if (!post) return;
  post.classList.add('unx-js');
  var redes = post.querySelectorAll('.unx-red');
  var tarjetas = post.querySelectorAll('.unx-g');
  for (var r = 0; r < redes.length; r++) {
    redes[r].addEventListener('click', function () {
      var p = this.getAttribute('data-p');
      for (var a = 0; a < redes.length; a++) redes[a].classList.toggle('activo', redes[a] === this);
      for (var b = 0; b < tarjetas.length; b++) tarjetas[b].classList.toggle('oculta', !!p && tarjetas[b].getAttribute('data-p') !== p);
    });
  }
  var ps = post.querySelectorAll('.unx-faq .p');
  for (var j = 0; j < ps.length; j++) {
    (function (p) {
      p.querySelector('.q').addEventListener('click', function () {
        var abrir = !p.classList.contains('abierta');
        for (var k = 0; k < ps.length; k++) ps[k].classList.remove('abierta');
        if (abrir) p.classList.add('abierta');
      });
    })(ps[j]);
  }
})();
</script>`;

// scripts/blog-entradas-bot.ts
async function datosEnVivo(id) {
  try {
    const r = await fetch(`https://uninexo.link/universidad/${id}`, { headers: { "user-agent": "UniNexoBlogBot/1.0 (+https://uninexo.link)" } });
    const m = (await r.text()).match(/id="datos-pagina">([\s\S]*?)<\/script>/);
    if (!m) return null;
    const d = JSON.parse(m[1]);
    return { materiales: d.materiales || [], academias: d.academias || [], docentes: d.docentes || [] };
  } catch {
    return null;
  }
}
var salida = process.argv[2] || "entradas.json";
var hoy = new Date(Date.now() - 5 * 36e5).toISOString().slice(0, 10).split("-").reverse().join("/");
var vacio = { materiales: [], academias: [], docentes: [] };
var entradas = [];
for (const u of PERU_UNIVERSITIES) {
  if ((armarPaginaUniversidad(u.id, vacio)?.grupos.length || 0) < 2) continue;
  const ext = await datosEnVivo(u.id);
  const p = ext && armarPaginaUniversidad(u.id, ext);
  const e = p && armarEntradaUniversidad(p, hoy);
  if (e) entradas.push(e);
  await new Promise((r) => setTimeout(r, 300));
}
writeFileSync(salida, JSON.stringify(entradas));
console.log(`RESUMEN ${JSON.stringify({ entradas: entradas.length, ids: entradas.map((e) => e.uniId) })}`);
