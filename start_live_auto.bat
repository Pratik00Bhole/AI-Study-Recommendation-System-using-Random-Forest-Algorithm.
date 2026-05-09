@echo off
setlocal

cd /d "%~dp0"

echo Starting always-on live mode...

if "%DATABASE_URL%"=="" set DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation

echo Ensuring MySQL database exists...
..\.venv\Scripts\python.exe backend\scripts\create_mysql_db.py
if errorlevel 1 (
  echo ERROR: Unable to prepare MySQL database.
  pause
  exit /b 1
)

echo Initializing backend tables...
..\.venv\Scripts\python.exe backend\scripts\init_db.py
if errorlevel 1 (
  echo ERROR: Unable to initialize database tables.
  pause
  exit /b 1
)

echo Checking database availability...
..\.venv\Scripts\python.exe -c "from sqlalchemy import create_engine, text; import os; engine = create_engine(os.environ['DATABASE_URL']); conn = engine.connect(); conn.execute(text('SELECT 1')); conn.close()" >nul 2>&1
if errorlevel 1 (
  echo Database is not reachable.
  echo Start MySQL and set DATABASE_URL correctly, then run this script again.

  ..\.venv\Scripts\python.exe -c "from sqlalchemy import create_engine, text; import os; engine = create_engine(os.environ['DATABASE_URL']); conn = engine.connect(); conn.execute(text('SELECT 1')); conn.close()" >nul 2>&1
  if errorlevel 1 (
    echo ERROR: Database is still unreachable.
    echo Example DATABASE_URL: mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation
    pause
    exit /b 1
  )
)

echo Database is reachable.

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

echo Starting backend watchdog...
start "AI Backend Watchdog" cmd /k "cd /d %~dp0 && start_backend_live.bat"

echo Starting frontend static server...
start "AI Frontend" cmd /k "cd /d %~dp0frontend\dist && python -m http.server 3000"

echo Live mode is running.
echo Frontend: http://localhost:3000
echo Backend API: http://127.0.0.1:8000/api

echo Use Ctrl+C inside each server window to stop it.
pause
