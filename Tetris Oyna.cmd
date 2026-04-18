@echo off
set "PYTHONW=C:\Users\ZG\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe"
set "PYGAME_HIDE_SUPPORT_PROMPT=1"
if not exist "%PYTHONW%" (
    powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Gerekli Python calisma zamani bulunamadi. Codex runtime klasoru silinmis olabilir.','Tetris')"
    exit /b 1
)
start "" "%PYTHONW%" "%~dp0tetris.py"
