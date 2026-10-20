# Quita la tarea programada del bot de Convocatorias (no borra nada más).
Unregister-ScheduledTask -TaskName 'UniNexo Bot Convocatorias' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host 'Tarea "UniNexo Bot Convocatorias" eliminada (si existía).'
