@echo off
REM LMS Backend Startup Script (No Reload)
REM This script starts the backend server without auto-reload

echo ========================================
echo   LMS Backend Server (Stable Mode)
echo ========================================
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start server WITHOUT reload
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

pause
