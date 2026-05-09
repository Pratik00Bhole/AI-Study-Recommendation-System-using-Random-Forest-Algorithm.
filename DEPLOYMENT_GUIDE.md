# AI Study Recommendation System - Deployment Guide

## Overview
This application consists of a Python Flask backend and a React frontend. For production deployment, we'll use Gunicorn for the backend and serve the frontend statically.

## Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL (for database)

## Demo Scope Aligned to Black Book
- Core deployment includes: Auth, Profile, Recommendations, Planner, Dashboard, Prediction, Adaptive Questions.
- Chatbot is intentionally disabled in production demo profile.
- MySQL is required for stable viva data persistence.

## Deployment Steps

### 0. Start MySQL and initialize tables (required)
Start MySQL service, create database `ai_study_recommendation`, then run:

```bash
cd backend
python scripts/init_db.py
```

### 1. Backend Deployment
```bash
cd backend
pip install -r requirements.txt
```

Run the backend:
- Windows: `set FLASK_ENV=production && set FLASK_DEBUG=false && set CHATBOT_ENABLED=false && set DB_REQUIRED=true && set DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation && ..\.venv\Scripts\python.exe -m waitress --listen=127.0.0.1:8000 wsgi:app`
- Linux/Mac: `FLASK_ENV=production FLASK_DEBUG=false CHATBOT_ENABLED=false DB_REQUIRED=true DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation gunicorn --bind 0.0.0.0:8000 wsgi:app`

### 2. Frontend Deployment
```bash
cd frontend
npm install
npm run build
```

Serve the `dist` folder with any static server (nginx, apache, etc.)

### 3. Environment Variables
Create a `.env` file in the backend directory:
```
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-strong-secret-key
JWT_SECRET_KEY=your-strong-jwt-secret
DATABASE_URL=mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation
CORS_ORIGINS=http://localhost:3000
DB_REQUIRED=true
CHATBOT_ENABLED=false
OPENAI_API_KEY=
```

Frontend production config in `frontend/.env.production`:
```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_ENABLE_CHATBOT=false
```

## Running for Final Year Project Demo

1. Start MySQL
2. Initialize DB: `cd backend && python scripts/init_db.py`
3. Run backend: `waitress-serve --host 127.0.0.1 --port 8000 wsgi:app`
4. Serve frontend: Use `python -m http.server 3000` in the `frontend/dist` directory
4. Access at http://localhost:3000

Health checks:
- Liveness: `GET /api/health`
- Readiness: `GET /api/health/ready`

## Note on Tomcat
Tomcat is a Java servlet container and is not suitable for Python Flask applications. If you need to deploy on a Java-based server, consider converting the backend to Java Spring Boot or using a different deployment strategy.