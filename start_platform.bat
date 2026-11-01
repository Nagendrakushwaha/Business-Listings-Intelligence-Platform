@echo off
title Business Listings Intelligence Platform - Launcher
echo ==========================================================
echo Launching Business Listings Intelligence Platform
echo ==========================================================
echo Starting Backend in a new window...
start "Business Listings Backend" cmd /c "%~dp0start_backend.bat"

echo Waiting 2 seconds for backend to initialize...
timeout /t 2 /nobreak > nul

echo Starting Frontend in a new window...
start "Business Listings Frontend" cmd /c "%~dp0start_frontend.bat"

echo.
echo Platform launched successfully!
echo Backend:  http://localhost:8000/docs
echo Frontend: http://localhost:5173/
echo.
pause
