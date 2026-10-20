# Quita la tarea programada del bot (no borra nada más).
Unregister-ScheduledTask -TaskName 'UniNexo Bot Empleos' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host 'Tarea "UniNexo Bot Empleos" eliminada (si existía).'
