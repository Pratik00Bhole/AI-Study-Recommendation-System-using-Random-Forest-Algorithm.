@echo off
REM AI Study Recommendation System - Demo Runner for Windows
setlocal

cd /d "%~dp0"

echo Starting AI Study Recommendation System Demo...

if not exist "frontend\dist\index.html" (
	echo Frontend build not found. Building frontend...
	cd frontend
	npm run build
	if errorlevel 1 (
		echo Frontend build failed.
		exit /b 1
	)
	cd ..
)

REM Start backend
echo Starting backend server...
start "AI Backend" cmd /k "cd /d %~dp0backend && set FLASK_ENV=production && set FLASK_DEBUG=false && set CHATBOT_ENABLED=false && set DB_REQUIRED=true && if "%DATABASE_URL%"=="" set DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation && set SECRET_KEY=demo-prod-secret-key-please-change-123456 && set JWT_SECRET_KEY=demo-prod-jwt-secret-key-please-change-123456 && ..\.venv\Scripts\python.exe -m waitress --listen=127.0.0.1:8000 wsgi:app"

REM Start frontend
echo Starting frontend server...
start "AI Frontend" cmd /k "cd /d %~dp0frontend\dist && python -m http.server 3000"

echo Demo running!
echo Frontend: http://localhost:3000
echo Backend API: http://127.0.0.1:8000/api
echo Close the command windows to stop

pause