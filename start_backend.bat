@echo off
title Business Listings Backend (FastAPI)
echo ==========================================================
echo Starting Business Listings Intelligence Backend (FastAPI)
echo ==========================================================

set PATH=%LOCALAPPDATA%\Programs\Python\Python313;%LOCALAPPDATA%\Programs\Python\Python313\Scripts;%PATH%
cd /d "%~dp0backend"

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo Swagger UI: http://localhost:8000/docs
echo Base API:   http://localhost:8000/api
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
