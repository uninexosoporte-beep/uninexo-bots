# Bot de Empleos de UniNexo

Vive en tu PC, revisa todos los días las páginas de empleo del Estado y te manda a **tu Telegram** solo lo nuevo.
**No publica nada por su cuenta:** tú decides qué publicar en UniNexo.

## Qué revisa (lista en `fuentes.json`)
1. **SERVIR · ofertas laborales**: las 25 regiones (CAS y 728). Es la fuente principal.
2. **SERVIR · prácticas** de todo el país.
3. **gob.pe**: búsqueda de convocatorias y las páginas de SUNARP, INDECOPI, INGEMMET, MTPE, MINEDU, MINJUS, MINEM, SUNAT, SERNANP, SERFOR, INIA, PNP y UNAMAD.
4. **Páginas vigiladas**: SUNARP (concursos CAS) e INDECOPI (comunicado de convocatorias).

## Reglas
- **Fechas:** solo avisa lo abierto que aún tenga 3 días o más (`dias_minimos_abierta`). Cada aviso trae la fecha de cierre y los días que faltan.
  Las publicaciones de gob.pe no traen cierre: se avisan si son de los últimos 3 días ("revisa las bases").
- **Sin duplicados:** guarda en `estado.sqlite` lo que ya avisó. Una oferta nunca se avisa dos veces; si la entidad **amplía** el plazo, se avisa otra vez marcada *AMPLIADA*.
  Tampoco avisa lo que ya está publicado en UniNexo.
- **Una sola vez al día y máximo 1 hora:** corre a la hora programada, avisa una vez y termina (normalmente en ~20 minutos). Si algo se demora, a los 50 minutos se frena, avisa lo que alcanzó y dice qué región faltó. Ese mismo día no vuelve a avisar (para repetir a mano: `python bot.py --forzar`).
- **Máximo 10 plazas por región** y 2 por entidad, las que cierran más tarde primero (y los CAS *indeterminados*, que son los contratos más largos, tienen prioridad).
- Sin plazas de limpieza, vigilancia, chofer, etc.; sueldo entre S/ 1,500 y S/ 30,000.

## Reglas por región y por carrera (en `config.json` → `"reglas"`)
```json
"reglas": {
  "regiones": { "solo": [], "ignorar": [], "prioritarias": ["Madre de Dios"], "tope_propio": {} },
  "carreras": { "solo": [], "ignorar": [], "incluir_sin_carrera": true },
  "cargos":   { "excluir_palabras": [], "incluir_palabras": [] }
}
```
- **Regiones:** `solo` (vacío = todas), `ignorar` (ni se leen), `prioritarias` (se leen primero y salen primero, con ⭐) y `tope_propio` para dar más o menos plazas a una región, por ejemplo `{"Madre de Dios": 15}`.
- **Carreras:** el bot deduce la carrera de cada plaza por las palabras de su cargo y la muestra como «🎓 Derecho». Con `solo` (por ejemplo `["Derecho", "Contabilidad"]`) avisa únicamente de esas carreras; con `ignorar` descarta las que no quieres. Si `solo` está vacío, solo etiqueta, no descarta nada.
  `incluir_sin_carrera: true` deja pasar los cargos ambiguos («Especialista III»); ponlo en `false` si prefieres no verlos.
- **Cargos:** `excluir_palabras` nunca avisa un cargo que contenga esa palabra (ej. `["secretaria"]`); `incluir_palabras` lo deja pasar siempre, aunque sea de otra carrera.
- Los nombres válidos de carrera salen con `python bot.py --reglas` (Derecho, Contabilidad, Economía, Administración, Educación, Medicina, Enfermería, Obstetricia, Odontología, Nutrición, Psicología, Trabajo Social, Farmacia y Química, Tecnología Médica, Biología, Ing. de Sistemas, Ing. Civil, Ing. Ambiental, Ing. Forestal, Agronomía y Veterinaria, Ing. Industrial / Eléctrica / Minas, Ciencias de la Comunicación, Turismo y Hotelería, Estadística, Antropología, Sociología y Arqueología, Gestión de Riesgos y Seguridad).
- Las reglas valen desde la próxima corrida (mañana a las 7:00). Una plaza se puede reconocer en varias carreras; las que el bot no reconoce quedan sin etiqueta. Las reglas de carrera también filtran los anuncios de gob.pe por su título.

## Lo que recibes
**Modo PDF (el que tienes activo):** cada día con novedades te llegan 3 cosas a Telegram: un resumen corto, el **informe en PDF** (plazas por región con cargo, entidad, sueldo, cierre y días que faltan, anuncios de gob.pe con enlaces, páginas con cambios) y el archivo `.json` para publicar.
El PDF lo crea Microsoft Edge (o Chrome) sin ventana: no hay que instalar nada. Si no se pudiera crear, ese día te manda los mensajes de texto de siempre y avisa por qué.
Se cambia con `"formato_aviso"` en `config.json`: `"pdf"`, `"mensajes"` (solo texto) o `"ambos"`.

Detalle de cada parte:
- Un mensaje con las plazas nuevas por región, otro con los anuncios de gob.pe (agrupados por institución), otro con las páginas que cambiaron y un resumen.
- Un archivo `nuevas-AAAA-MM-DD.json` con las plazas en el formato de UniNexo (queda también en la carpeta `salida/`).
  Para publicarlas: pásaselo a Claude («publica este archivo en Empleos del Estado»).
- Si un día no hay nada nuevo, un mensaje corto «sin novedades» (se apaga con `avisar_si_no_hay_novedades: false` en `config.json`).
- Si algo falla (por ejemplo SERVIR no responde) te lo dice por Telegram.

## Comandos (desde `D:\uninexo-bot`)
| Para… | Comando |
|---|---|
| Probar que llega a tu Telegram | `python bot.py --prueba` |
| Ver qué mandaría, sin enviar ni guardar nada | `python bot.py --simular --ver-formato --solo Arequipa --sin-gobpe --sin-paginas --sin-practicas` |
| Ver tus reglas de región y carrera y las carreras disponibles | `python bot.py --reglas` |
| Correrlo a mano | `python bot.py` |
| Volver a "aprender" lo que existe hoy sin avisar | `python bot.py --baseline` |
| Programarlo todos los días | `.\instalar_tarea.ps1 -Hora 07:00` |
| Quitar la programación | `.\desinstalar_tarea.ps1` |
| Pruebas del código | `python -m unittest discover -s tests` |

La **primera corrida** solo aprende lo que ya existe (para no llenarte el chat) y te manda un mensaje de "listo". Desde la segunda avisa solo lo nuevo.
Tarda unos 20 minutos porque deja pausas largas entre consultas a SERVIR (así no lo satura).

## Seguridad
- El token de tu bot y tu chat están en `.env` (no se sube a ningún lado). Si crees que se filtró: en `@BotFather` envía `/revoke`, elige tu bot, copia el token nuevo y cámbialo en la línea `TELEGRAM_BOT_TOKEN=` del `.env`.
- El bot solo **lee** páginas públicas y solo **escribe** a tu chat de Telegram.
- Para que no se acumulen archivos, puedes borrar de `logs/` y `salida/` lo viejo cuando quieras.

## Si una página cambia y el bot deja de leerla
Te llegará un aviso «No pude leer…». Los textos mal escritos del portal se corrigen en `normalizar.py` (listas `ENTIDADES`, `DISTRITOS`, `CARGOS`).
Para agregar una página a vigilar, copia un bloque `"tipo": "vigilada"` de `fuentes.json`.

## Publicación automática en la web (20/10/2026)
Al terminar cada corrida, el bot sube las plazas a Empleos del Estado de uninexo.link (`publicar_web.py`). Usa el publicador del proyecto (`D:\uninexo\scripts\publicar-empleos-bot.ts`) con la cuenta `bot-empleos@uninexo.link`, que SOLO puede crear plazas. Necesita en este `.env`: `UNINEXO_BOT_PASSWORD=...` (la contraseña de esa cuenta; nunca la compartas). Se apaga poniendo `"activa": false` en `config.json` → `publicacion_automatica`. Cada día pasa los archivos de los últimos 7 días: lo ya publicado se salta, así que un día con error se recupera al siguiente. El resultado sale en el aviso de Telegram («🌐 Publiqué N plazas»).
