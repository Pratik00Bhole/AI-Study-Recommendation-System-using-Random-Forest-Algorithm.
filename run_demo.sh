#!/bin/bash

# AI Study Recommendation System - Demo Runner
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "Starting AI Study Recommendation System Demo..."

if [ ! -f "frontend/dist/index.html" ]; then
	echo "Frontend build not found. Building frontend..."
	cd frontend
	npm run build
	cd ..
fi

# Start backend
echo "Starting backend server..."
cd backend
FLASK_ENV=production FLASK_DEBUG=false CHATBOT_ENABLED=false SECRET_KEY='demo-prod-secret-key-please-change-123456' JWT_SECRET_KEY='demo-prod-jwt-secret-key-please-change-123456' gunicorn --bind 0.0.0.0:8000 wsgi:app &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend/dist
python -m http.server 3000 &
FRONTEND_PID=$!

echo "Demo running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://127.0.0.1:8000/api"
echo "Press Ctrl+C to stop"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait