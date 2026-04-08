@echo off
setlocal

echo Starting Django Backend Server...

:: Check for venv (one level up)
if exist "%~dp0..\venv\Scripts\python.exe" (
    echo [INFO] Using environment at "%~dp0..\venv\Scripts\python.exe"
    "%~dp0..\venv\Scripts\python.exe" "%~dp0manage.py" runserver 0.0.0.0:8001
    goto :end
)

:: Check for env (one level up)
if exist "%~dp0..\env\Scripts\python.exe" (
    echo [INFO] Using environment at "%~dp0..\env\Scripts\python.exe"
    "%~dp0..\env\Scripts\python.exe" "%~dp0manage.py" runserver 0.0.0.0:8001
    goto :end
)

echo [ERROR] No virtual environment found! 
echo Please make sure you have a 'venv' or 'env' folder in the parent directory.
pause

:end
endlocal
