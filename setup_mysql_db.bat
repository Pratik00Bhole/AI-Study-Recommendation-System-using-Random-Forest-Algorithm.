@echo off
setlocal

cd /d "%~dp0"

if "%DATABASE_URL%"=="" set DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation

echo Creating MySQL database if it does not exist...
.\.venv\Scripts\python.exe backend\scripts\create_mysql_db.py
if errorlevel 1 (
  echo Database creation failed.
  pause
  exit /b 1
)

echo Initializing backend tables...
.\.venv\Scripts\python.exe backend\scripts\init_db.py
if errorlevel 1 (
  echo Table initialization failed.
  pause
  exit /b 1
)

echo MySQL setup complete.
echo DATABASE_URL=%DATABASE_URL%
pause
