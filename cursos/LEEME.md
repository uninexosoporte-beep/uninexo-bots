# Bot de Cursos y Oportunidades de UniNexo

Vive en tu PC (`D:\uninexo-bot-cursos`), revisa cada día gob.pe y varias páginas de becas y te manda a **tu Telegram (bot «CURSO UNINEXO 1»)** solo lo nuevo.
**No publica nada por su cuenta:** lo que encuentra va a la **cola de revisión** de la sección Cursos y tú apruebas cada cosa.
Es independiente del bot de Empleos (`D:\uninexo-bot`, bot «Profe Jhon»): otra carpeta, otra memoria, otro token. Sus mensajes empiezan con 📚.

## Qué revisa (lista en `fuentes.json`)
1. **gob.pe · campañas** de 32 instituciones nacionales (PRONABEC, SERVIR, MTPE, CONCYTEC, MINEDU, SENCICO, SERFOR, INIA, OSIPTEL, SUNASS, Osinergmin, INDECOPI, Cultura, MINAM, PRODUCE, MINSA, SUNEDU, SENAMHI, IGP, INEI, SUNAT, Contraloría, MIDIS, MIMP, MEF, MINJUS, INS, SERNANP, SENASA, OEFA, ANA y **UNAMAD**).
2. **gob.pe · búsqueda** de becas, concursos de becas, cursos virtuales gratuitos, capacitaciones, diplomados, programas de extensión, talleres, webinars, voluntariados y especializaciones.
3. **13 páginas de becas y programas vigiladas**: PRONABEC (3), Fulbright, Fundación Carolina, OEA, ProInversión, Osinergmin, OSIPTEL, UNI, SENAJU, UNICEF y PROCIENCIA. Avisa si aparece una novedad (por ejemplo «abierta la convocatoria 2027»).

De cada oportunidad nueva abre su página y lee, **solo si lo dice**: si es gratis (o su costo), la fecha límite y la modalidad. Lo que la página no dice no se inventa: el costo queda «Por confirmar» y sin fecha límite.

## Reglas (en `config.json` → `"reglas"`)
```json
"reglas": {
  "tipos": { "solo": [], "ignorar": [] },
  "areas": { "solo": [], "ignorar": [] },
  "solo_gratuitos": false,
  "incluir_costo_desconocido": true,
  "dias_minimos_abierta": 2,
  "instituciones": { "incluir": ["unamad"], "ignorar": [] },
  "incluir_locales": false,
  "palabras_excluir": []
}
```
- **tipos:** `beca`, `curso`, `diplomado`, `especializacion`, `certificacion`, `taller`, `webinar`, `convocatoria`, `experiencia_laboral`, `voluntariado` (los de la sección Cursos). Ej.: `"solo": ["beca", "curso"]`.
- **areas:** las de la sección (Salud, Derecho y Ciencias Políticas, Tecnología e Informática, Idiomas…); `python bot.py --reglas` las lista. Lo que no tiene un área clara pasa igual.
- **solo_gratuitos:** `true` descarta lo que la página dice que es de pago; `incluir_costo_desconocido` decide si pasa lo que no dice nada del costo.
- **instituciones:** `incluir` (se leen y pasan aunque sean locales; hoy `unamad`) e `ignorar`. Las **locales** (municipios, UGEL, gobiernos regionales, hospitales) se ignoran por defecto; `incluir_locales: true` las abre.
- **palabras_excluir:** nunca avisa un título que las tenga.
- Siempre aplica: nada de plazas de trabajo (eso es del bot de Empleos), resultados, listas de admitidos ni notas de prensa; lo ya publicado en Cursos no se repite (mismo enlace o casi el mismo nombre en la misma institución).

## Cómo respeta fechas y duplicados
- Solo avisa lo publicado en los últimos 3 días (`dias_recientes`) que no haya visto antes. Con fecha límite en la página, exige 2 días de margen; lo vencido se ignora.
- Memoria en `estado.sqlite`: cada oportunidad se identifica por su enlace y por institución + título. Nunca la avisa dos veces.
- **Una sola vez al día y máximo 1 hora** (normalmente tarda ~5 minutos). Ese día no vuelve a avisar (para repetir: `python bot.py --forzar`).
- La **primera corrida** solo aprende lo que ya existe y te manda un mensaje de «listo»; desde la segunda avisa solo lo nuevo.

## Lo que recibes (con novedades)
1. Un resumen corto (nuevas, cuántas gratuitas, páginas con cambios).
2. **El informe en PDF**: oportunidades por tipo (becas primero), con costo, fecha de cierre y días que faltan, modalidad y enlace. Lo crea Edge o Chrome, que ya están en tu PC.
3. Un archivo `candidatas-AAAA-MM-DD.json` para el botón **«Importar del bot»** de la sección Cursos: van a la **cola de revisión**; ahí las apruebas o rechazas.
Sin novedades: un mensaje corto («no hay novedades»). Si algo falla, te avisa por Telegram.

## Comandos (desde `D:\uninexo-bot-cursos`)
| Para… | Comando |
|---|---|
| Probar que llega a tu Telegram | `python bot.py --prueba` |
| Ver tus reglas y los tipos/áreas válidos | `python bot.py --reglas` |
| Ver qué mandaría hoy, sin enviar ni guardar nada | `python bot.py --simular --ver-formato --dias 30 --sin-paginas` |
| Correrlo a mano | `python bot.py` |
| Volver a «aprender» lo que existe sin avisar | `python bot.py --baseline` |
| Programarlo todos los días a las 08:00 | `.\instalar_tarea.ps1` |
| Quitar la programación | `.\desinstalar_tarea.ps1` |
| Pruebas del código | `python -m unittest discover -s tests` |

## Seguridad
- El token y tu chat están en `.env` (no sale de tu PC). Si crees que se filtró: en `@BotFather` envía `/revoke`, elige **CURSO UNINEXO 1** y cambia la línea `TELEGRAM_BOT_TOKEN=` del `.env`.
- El bot solo **lee** páginas públicas y solo **escribe** a tu chat de Telegram.
- Sin Claude y sin internet de pago: es un programa de Python común. Si una página cambia de diseño, el bot te avisa «No pude leer…» y hay que ajustarlo.

## Páginas que no se pueden revisar solas
DAAD y PNUD (bloquean programas automáticos), Gates Cambridge y Erasmus Mundus (se arman con JavaScript), Chevening y la ENAP (tardaron en responder; la ENAP publica en gob.pe/servir, que sí se revisa), y plataformas privadas como Coursera o edX (sus términos de uso prohíben copiar el catálogo).

## Filtro de noticias (20/10/2026)
De 50 candidatas en 8 días, ~40 eran notas de prensa. Ahora `clasificar.py` descarta: títulos que cuentan algo que ya pasó o que solo informan (`NOTICIA`: «realizó», «participaron», «fortalece», «impulsa», «obtiene»…; se compara sin tildes), títulos dirigidos a personal, trabajadores o beneficiarios (`SOLO_PERSONAL_TITULO`), premios que no son para estudiantes o jóvenes, eventos con una fecha pasada escrita en palabras («15 de octubre») y hospitales nacionales (`LOCALES`: hn, hma, hlev…). Al leer la página, si dice que es solo para personal de una entidad (`SOLO_PERSONAL`: «dirigido a funcionarios», «vínculo laboral», «oficio de la entidad») y no invita a estudiantes ni a la ciudadanía (`ABIERTO`), se descarta. Pruebas: `TestRuidoDeNoticias` en `tests/test_bot.py`.

## Aprobar cursos con un toque (20/10/2026)
Cada curso candidato llega como un mensaje con ✅ Publicar / ❌ Descartar. Cada 30 minutos (`python bot.py --aprobaciones`, tarea instalada con `instalar_tarea_aprobaciones.ps1`) se leen tus toques: ✅ se publica en uninexo.link/cursos como «sugerido» y el mensaje cambia a «✅ Publicado»; ❌ se olvida. Solo valen los toques de tu propio chat. Lo que no tocas en 14 días vence. Se apaga con `"activa": false` en `config.json` → `aprobacion_telegram`.
