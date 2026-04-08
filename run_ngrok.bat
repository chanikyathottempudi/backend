@echo off
set "NGROK_PATH=c:\Users\lenovo\Downloads\ngrok-v3-stable-windows-amd64\ngrok.exe"
set "DOMAIN=tommy-gemmier-bruno.ngrok-free.dev"
set "PORT=8000"

echo Starting ngrok tunnel for %DOMAIN% on port %PORT%...
echo.

if not exist "%NGROK_PATH%" (
    echo Error: ngrok.exe not found at %NGROK_PATH%
    pause
    exit /b 1
)

:: Try to start ngrok
"%NGROK_PATH%" http --domain=%DOMAIN% %PORT%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo -----------------------------------------------------------
    echo ERROR: ngrok failed to start.
    echo This usually happens if you haven't added your authtoken yet.
    echo.
    echo 1. Get your authtoken here: https://dashboard.ngrok.com/get-started/your-authtoken
    echo 2. Run this command (replace YOUR_TOKEN with the actual token):
    echo    "%NGROK_PATH%" config add-authtoken YOUR_TOKEN
    echo -----------------------------------------------------------
)

pause
