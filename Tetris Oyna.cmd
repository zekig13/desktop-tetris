@echo off
set "PYGAME_HIDE_SUPPORT_PROMPT=1"
set "SCRIPT=%~dp0tetris.py"

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%SCRIPT%"
    exit /b 0
)

where pyw >nul 2>nul
if %errorlevel%==0 (
    start "" pyw "%SCRIPT%"
    exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
    start "" python "%SCRIPT%"
    exit /b 0
)

powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Python bulunamadi. Oyunu calistirmak icin Python 3 kurup tekrar deneyin.','Tetris')"
exit /b 1
