@echo off
REM LMS Backend Startup Script with Auto-Reload
REM This version uses --reload-dir to avoid infinite loops

echo ========================================
echo   LMS Backend Server (Auto-Reload Mode)
echo ========================================
echo.
echo Starting server on http://127.0.0.1:8000
echo Auto-reload enabled (watching 'app' directory only)
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start server WITH reload but only watching app directory
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app

pause
