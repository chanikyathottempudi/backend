# Simplified startup script for CT Dose Monitoring Backend
Write-Host "Starting Django Backend Server..." -ForegroundColor Green

# Check for venv (one level up)
$VENV_PYTHON = "$PSScriptRoot\..\venv\Scripts\python.exe"
if (Test-Path $VENV_PYTHON) {
    Write-Host "[INFO] Using environment at $VENV_PYTHON" -ForegroundColor Cyan
    & $VENV_PYTHON "$PSScriptRoot\manage.py" runserver 0.0.0.0:8000
    exit
}

# Check for env (one level up)
$ENV_PYTHON = "$PSScriptRoot\..\env\Scripts\python.exe"
if (Test-Path $ENV_PYTHON) {
    Write-Host "[INFO] Using environment at $ENV_PYTHON" -ForegroundColor Cyan
    & $ENV_PYTHON "$PSScriptRoot\manage.py" runserver 0.0.0.0:8000
    exit
}

Write-Error "[ERROR] No virtual environment found! Please ensure 'venv' or 'env' exists in the parent directory."
Read-Host "Press Enter to exit..."
