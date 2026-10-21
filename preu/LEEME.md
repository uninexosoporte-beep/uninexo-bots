# Bot Preu (uninexo.link/preu)

Mantiene al día la sección **Preu** (para escolares que van a postular). **No publica nada solo.**

| Qué hace | Cuándo | Qué te llega por Telegram |
|---|---|---|
| Lee el cronograma de **Beca 18** en la web del PRONABEC | Lunes 08:00 (Perú) | Si cambió: las fechas nuevas con **✅ Publicar / ❌ Descartar** |
| Mira **«En proceso»** en la página de concursos del PRONABEC | Lunes 08:00 | Si apareció un concurso nuevo: su nombre y enlace (solo aviso) |
| Prueba los **enlaces oficiales** de Preu y las webs de las universidades (`enlaces.json`) | Lunes 08:00 | Los que fallan **2 semanas seguidas**, y cuando vuelven |
| Lee tus toques ✅/❌ y publica lo aprobado | Cada 2 horas | El mensaje cambia a «✅ Publicado» |

- Siempre manda un resumen semanal («🎓 Bot Preu · revisión semanal»), aunque no haya cambios.
- La **primera corrida solo aprende** lo que hay (no avisa nada).
- Con ✅, el cronograma se guarda en Firestore `preu_config/beca18` con la cuenta bot. La web lo muestra en hasta 6 horas
  (cada celular guarda una copia 6 h). Las reglas solo dejan a la cuenta bot escribir ESE documento, con la forma exacta.
- Lo que no tocas en 21 días vence y no se publica.

## Credenciales
- Telegram: el **bot de Convocatorias** (en GitHub, el Secret `CONVOCATORIAS_ENV`; en la PC, un `.env` aquí con
  `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`). Nadie más lee las respuestas de ese bot, así que los botones no chocan.
- Cuenta bot de Firestore: la del bot de empleos (`UNINEXO_CREDENCIALES` o `config.json` → `credenciales`).

## Mantenimiento
- `enlaces.json` y `../publicador/publicar-preu-bot.mjs` salen del proyecto: `npm run empaquetar:bots` en `D:\uninexo`.
- Si el PRONABEC cambia el diseño de su página, el bot avisa «no pude leer» en vez de publicar algo raro: hay que
  ajustar `pronabec.py` (y sus pruebas con la página nueva en `tests/fixtures`).
- Pruebas: `python -m unittest discover -s tests` (desde esta carpeta).
- Memoria: `estado.json` (se guarda en el repositorio después de cada corrida).
