# Bot de Convocatorias de UniNexo

Vive en tu PC (`D:\uninexo-bot-convocatorias`), revisa cada día gob.pe y varios programas y te manda a **tu Telegram (bot «COMBOCATORIAS UNINEXO», `@COMBOCATORIASUNINEXOBOT`)** solo lo nuevo.
**No publica nada por su cuenta:** te manda un archivo y tú decides qué publicar con el botón **«Importar del bot»** de la pestaña Convocatorias (todo entra desmarcado).
Es independiente del bot de Empleos (`D:\uninexo-bot`, «Profe Jhon») y del de Cursos (`D:\uninexo-bot-cursos`, «CURSO UNINEXO 1»): otra carpeta, otra memoria, otro token. Sus mensajes empiezan con 💼.

## Qué busca
Voluntariados, prácticas pre y profesionales, part-time y programas de primer empleo / empleo joven (ferias laborales, jóvenes profesionales…) de instituciones del Estado.
Los procesos CAS y las plazas del Estado **no** (eso es del bot de Empleos): el tipo `cas` está en `"ignorar"`.

## Qué revisa (lista en `fuentes.json`)
1. **gob.pe · campañas** de 42 instituciones nacionales (SERVIR, MTPE, MINEDU, MIMP, MINAM, MIDIS, Ministerio Público, RENIEC, EsSalud, INDECOPI, OSIPTEL, Osinergmin, SUNARP, MEF, MINJUS, MINSA, Cultura, PRODUCE, PRONABEC, SUNEDU, CONCYTEC, INEI, SENAMHI, SERNANP, SENASA, OEFA, ANA, Contraloría, Cancillería, MTC, Vivienda, MINCETUR, INDECI, IPD, DEVIDA, SUTRAN, ANIN, Poder Judicial, SMV, JNE, ONPE y **UNAMAD**).
2. **gob.pe · búsqueda** de «programa de voluntariado», «convocatoria voluntariado», «voluntarios», «convocatoria de prácticas», «practicantes», «prácticas preprofesionales», «prácticas profesionales», «modalidades formativas», «pasantías», «part time», «feria laboral», «primer empleo» y «jóvenes profesionales».
3. **4 páginas de programas vigiladas**: SENAJU (voluntariado juvenil), Cruz Roja Peruana, Registro de Voluntariado (Sinavol, MIMP) y Empleos Perú. Avisa si aparece una novedad (por ejemplo «abierta la convocatoria»).

## Las prácticas se avisan por ENTIDAD, no una por una
INDECOPI saca más de 60 convocatorias de prácticas al año y el MIMP más de 90: avisar cada una te llenaría el chat y UniNexo ya enlaza la lista de cada entidad.
Por eso, cuando el bot ve una convocatoria de prácticas de una entidad que **todavía no está en la pestaña Convocatorias**, te propone **una sola ficha** «Prácticas pre y profesionales en <entidad>» (con el enlace de esa convocatoria). Si la importas, esa entidad ya no se vuelve a proponer.

## Reglas (en `config.json` → `"reglas"`)
```json
"reglas": {
  "tipos": { "solo": [], "ignorar": ["cas"] },
  "dias_minimos_abierta": 2,
  "instituciones": { "incluir": ["unamad"], "ignorar": [] },
  "incluir_locales": false,
  "palabras_excluir": []
}
```
- **tipos:** `practicas`, `voluntariado`, `part_time`, `full_time`, `cas` (los de la pestaña Convocatorias). Ej.: `"solo": ["voluntariado"]`.
- **instituciones:** `incluir` (se leen y pasan aunque sean locales; hoy `unamad`) e `ignorar`. Las **locales** (municipios, UGEL, gobiernos regionales, hospitales) se ignoran por defecto; `incluir_locales: true` las abre.
- **palabras_excluir:** nunca avisa un título que las tenga.
- Siempre aplica: nada de resultados, listas de admitidos, comunicados, «buenas prácticas» ni notas de prensa; lo ya publicado en Convocatorias no se repite (mismo enlace, misma entidad o casi el mismo título).

## Cómo respeta fechas y duplicados
- Solo avisa lo publicado en los últimos 7 días (`dias_recientes`) que no haya visto antes. Con fecha límite en la página, exige 2 días de margen; lo vencido se ignora. Si la página no dice fecha, no se inventa: sale «sin fecha en la página».
- Memoria en `estado.sqlite`: cada convocatoria se identifica por su enlace y por institución + título. Nunca la avisa dos veces.
- **Una sola vez al día y máximo 1 hora** (normalmente tarda ~10 minutos). Ese día no vuelve a avisar (para repetir: `python bot.py --forzar`).
- La **primera corrida** solo aprende lo que ya existe y te manda un mensaje de «listo»; desde la segunda avisa solo lo nuevo (hasta 30 por día; lo que sobra pasa al día siguiente).

## Lo que recibes (con novedades)
1. Un resumen corto (convocatorias nuevas, entidades nuevas, programas con cambios).
2. **El informe en PDF**: convocatorias por tipo (voluntariados y prácticas primero), con fecha de cierre y días que faltan, modalidad, lugar y enlace. Lo crea Edge o Chrome, que ya están en tu PC.
3. Un archivo `candidatas-AAAA-MM-DD.json` para el botón **«Importar del bot»** de la pestaña Convocatorias (solo admin). Ahí ves cada una con su enlace, marcas las que sirven y se publican como **«Detectada automáticamente»** (sin la insignia «Verificado»).
Sin novedades: un mensaje corto («no hay novedades»). Si algo falla, te avisa por Telegram.

## Comandos (desde `D:\uninexo-bot-convocatorias`)
| Para… | Comando |
|---|---|
| Probar que llega a tu Telegram | `python bot.py --prueba` |
| Ver tus reglas y los tipos válidos | `python bot.py --reglas` |
| Ver qué mandaría hoy, sin enviar ni guardar nada | `python bot.py --simular --ver-formato --dias 30 --sin-paginas` |
| Correrlo a mano | `python bot.py` |
| Volver a «aprender» lo que existe sin avisar | `python bot.py --baseline` |
| Programarlo todos los días a las 09:00 (hora de la PC) | `.\instalar_tarea.ps1` |
| Quitar la programación | `.\desinstalar_tarea.ps1` |
| Pruebas del código | `python -m unittest discover -s tests` |

## Seguridad
- El token y tu chat están en `.env` (no sale de tu PC). Si crees que se filtró: en `@BotFather` envía `/revoke`, elige **COMBOCATORIAS UNINEXO** y cambia la línea `TELEGRAM_BOT_TOKEN=` del `.env`.
- El bot solo **lee** páginas públicas y solo **escribe** a tu chat de Telegram.
- Sin Claude y sin internet de pago: es un programa de Python común. Si una página cambia de diseño, el bot te avisa «No pude leer…» y hay que ajustarlo.

## Páginas que no se pueden revisar solas
SUNAT, BCP, ONPE y BCRP (responden 403 o piden «verificar que eres humano»: bloquean programas automáticos), Lima 2027 (su sitio responde igual a cualquier ruta y no deja ver el contenido) y los portales de empleo de empresas privadas (se arman con JavaScript o piden iniciar sesión; sus avisos están en Bumeran o LinkedIn).

## Publicación automática en la web (20/10/2026)
Al terminar cada corrida, el bot publica las candidatas en Convocatorias de uninexo.link como «Detectada automáticamente» (`publicar_web.py`). Usa el publicador del proyecto (`D:\uninexo\scripts\publicar-convocatorias-bot.ts`), que descarta notas de prensa y repetidas, con la cuenta bot de UniNexo. Sus credenciales NO están aquí: se leen de `D:\uninexo-bot\.env` (`config.json` → `publicacion_automatica.credenciales`). `publicados_web.json` guarda los archivos ya publicados: lo que borres en la web no vuelve. Se apaga con `"activa": false`.
