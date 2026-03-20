@echo off
REM Web Scraper & Summarizer - Windows Startup Script

echo.
echo Web Scraper ^& Summarizer - Startup Script
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env and add your API keys:
    echo   - NVIDIA_API_KEY
    echo   - BRAVE_SEARCH_API_KEY
    echo.
    pause
    exit /b 1
)

REM Start backend
echo Starting backend...
cd backend

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing backend dependencies...
pip install -q -r requirements.txt

REM Start backend in new window
echo Backend starting on http://localhost:8000
start "Backend" python main.py

cd ..

REM Start frontend
echo Starting frontend...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install -q
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    copy .env.local.example .env.local
)

echo Frontend starting on http://localhost:3000
start "Frontend" cmd /k npm run dev

cd ..

echo.
echo Both services started!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
