# Quita la tarea programada del bot de Cursos (no borra nada más).
Unregister-ScheduledTask -TaskName 'UniNexo Bot Cursos' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host 'Tarea "UniNexo Bot Cursos" eliminada (si existía).'
