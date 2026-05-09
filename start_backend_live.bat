@echo off
setlocal

cd /d "%~dp0backend"

set FLASK_ENV=production
set FLASK_DEBUG=false
set CHATBOT_ENABLED=false
set DB_REQUIRED=true
set SECRET_KEY=demo-prod-secret-key-please-change-123456
set JWT_SECRET_KEY=demo-prod-jwt-secret-key-please-change-123456

if "%DATABASE_URL%"=="" set DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation

echo [%date% %time%] Checking database connectivity...
..\.venv\Scripts\python.exe -c "from sqlalchemy import create_engine, text; import os; engine = create_engine(os.environ['DATABASE_URL']); conn = engine.connect(); conn.execute(text('SELECT 1')); conn.close(); print('Database reachable')"
if errorlevel 1 (
	echo [%date% %time%] ERROR: Database is not reachable.
	echo Start MySQL first and verify DATABASE_URL, then run this script again.
	pause
	exit /b 1
)

:start_server
echo [%date% %time%] Starting backend server on http://127.0.0.1:8000
..\.venv\Scripts\python.exe -m waitress --listen=127.0.0.1:8000 wsgi:app

echo [%date% %time%] Backend stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto start_server
