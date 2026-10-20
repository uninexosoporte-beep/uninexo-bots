# Bots de UniNexo Perú

Tres bots que buscan oportunidades para universitarios del Perú en fuentes oficiales (SERVIR, gob.pe) y las publican en [uninexo.link](https://uninexo.link). Corren solos en GitHub Actions; avisan por Telegram.

| Bot | Carpeta | Cuándo (hora de Perú) | Qué publica |
|---|---|---|---|
| Empleos del Estado | `empleos/` | 00:00 | Plazas CAS y prácticas de SERVIR, solo en Empleos del Estado |
| Cursos | `cursos/` | 01:00 + cada 2 h | Cada curso llega a Telegram con ✅/❌; se publica solo lo aprobado |
| Convocatorias | `convocatorias/` | 02:00 | Voluntariados y prácticas de gob.pe, como «Detectada automáticamente» |

- `publicador/`: los publicadores del proyecto UniNexo empaquetados (un archivo cada uno, solo Node). Validan cada dato igual que la web y entran con una **cuenta bot sin permisos de administrador**: las reglas de Firestore solo le dejan **crear** con el formato exacto (no edita ni borra).
- Las credenciales (tokens de Telegram, cuenta bot, App Check) están **solo en los Secrets** del repositorio: `EMPLEOS_ENV`, `CURSOS_ENV`, `CONVOCATORIAS_ENV`.
- La memoria de cada bot (`estado.sqlite`, `salida/*.json`, `aprobaciones.json`, `publicados_web.json`) se guarda en el repositorio al final de cada corrida, para no repetir avisos.
- Para correr uno a mano: pestaña **Actions** → el bot → **Run workflow**.
- Si cambian las validaciones de la web: en el proyecto, `npm run empaquetar:bots` y subir `publicador/` de nuevo.
