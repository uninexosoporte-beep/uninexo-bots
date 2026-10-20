# Programa la revisión de tus toques ✅/❌ del bot de Cursos: cada 30 minutos mientras la PC esté prendida.
# Lee los botones que tocaste en Telegram y publica en uninexo.link lo aprobado (ver aprobaciones.py). Cada vuelta dura segundos.
#   .\instalar_tarea_aprobaciones.ps1                -> cada 30 minutos
#   .\instalar_tarea_aprobaciones.ps1 -Minutos 15    -> cada 15 minutos
# Para quitarla:  Unregister-ScheduledTask -TaskName 'UniNexo Cursos Aprobaciones' -Confirm:$false
param([int]$Minutos = 30)

$carpeta = $PSScriptRoot
$python = (& python -c "import sys; print(sys.executable)").Trim()
$pythonw = Join-Path (Split-Path $python) 'pythonw.exe'
if (Test-Path $pythonw) { $python = $pythonw }

$accion = New-ScheduledTaskAction -Execute $python -Argument 'bot.py --aprobaciones' -WorkingDirectory $carpeta
$disparador = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $Minutos)
$ajustes = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName 'UniNexo Cursos Aprobaciones' -Action $accion -Trigger $disparador -Settings $ajustes `
    -Description 'Lee los toques de aprobar/descartar cursos en Telegram y publica lo aprobado en uninexo.link.' -Force | Out-Null

Write-Host "Listo: revisaré tus toques de Telegram cada $Minutos minutos."
