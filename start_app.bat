@echo off
echo Starting Quantum Learning Platform...

:: Start Backend
start "Quantum Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8001"

:: Start Frontend
start "Quantum Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Application starting...
echo Frontend will be at: http://localhost:3000
echo Backend will be at: http://localhost:8001
echo.
pause
