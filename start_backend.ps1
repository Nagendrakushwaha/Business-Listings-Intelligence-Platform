Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Starting Business Listings Intelligence Backend (FastAPI)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$env:PATH = "$env:LOCALAPPDATA\Programs\Python\Python313;$env:LOCALAPPDATA\Programs\Python\Python313\Scripts;" + $env:PATH
Set-Location -Path "$PSScriptRoot\backend"

if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
}

Write-Host "API Swagger UI: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "API Endpoint  : http://localhost:8000/api" -ForegroundColor Green

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

