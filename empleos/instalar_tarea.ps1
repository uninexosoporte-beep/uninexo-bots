# Programa el bot para que Windows lo ejecute solo una vez al día.
#   .\instalar_tarea.ps1                 -> todos los días a las 07:00
#   .\instalar_tarea.ps1 -Hora 06:30     -> a otra hora
# Si la PC estaba apagada a esa hora, el bot corre apenas se enciende ("StartWhenAvailable").
# Para quitarla: .\desinstalar_tarea.ps1
param([string]$Hora = '07:00')

$carpeta = $PSScriptRoot
# Ruta REAL de Python (no el acceso directo de la tienda de Windows, que a veces falla dentro de una tarea programada)
$python = (& python -c "import sys; print(sys.executable)").Trim()
# pythonw no abre ventana negra; si no existe se usa python normal
$pythonw = Join-Path (Split-Path $python) 'pythonw.exe'
if (Test-Path $pythonw) { $python = $pythonw }

$accion = New-ScheduledTaskAction -Execute $python -Argument 'bot.py' -WorkingDirectory $carpeta
$disparador = New-ScheduledTaskTrigger -Daily -At $Hora
$ajustes = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName 'UniNexo Bot Empleos' -Action $accion -Trigger $disparador -Settings $ajustes `
    -Description 'Revisa SERVIR, gob.pe y páginas de empleo del Estado y avisa por Telegram solo lo nuevo.' -Force | Out-Null

Write-Host "Listo: el bot correrá todos los días a las $Hora."
Write-Host 'Para probarlo ya mismo:  Start-ScheduledTask -TaskName "UniNexo Bot Empleos"'
