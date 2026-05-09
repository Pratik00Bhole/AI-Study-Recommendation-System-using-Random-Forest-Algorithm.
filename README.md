# AI Study Recommendation System

A full-stack AI-powered study recommendation platform using Flask, React, MySQL, Scikit-learn, and hybrid NLP (TF-IDF + BERT embeddings).

## Tech Stack

- Backend: Flask + JWT + SQLAlchemy
- Frontend: React (Vite) + Axios + Recharts
- Database: MySQL
- Machine Learning: Scikit-learn (Random Forest)
- NLP: TF-IDF + Sentence-BERT (`all-MiniLM-L6-v2`)
- Chatbot Tutor: OpenAI GPT API

## Folder Structure

```text
AI Study Recommendation System/
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── data_catalog.py
│   │   │   ├── model_pipeline.py
│   │   │   └── nlp_engine.py
│   │   ├── models/
│   │   │   ├── user_model.py
│   │   │   ├── student_profile_model.py
│   │   │   └── progress_model.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── student_routes.py
│   │   │   ├── recommendation_routes.py
│   │   │   ├── planner_routes.py
│   │   │   ├── progress_routes.py
│   │   │   ├── prediction_routes.py
│   │   │   ├── adaptive_routes.py
│   │   │   └── chatbot_routes.py
│   │   ├── services/
│   │   ├── utils/
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   ├── ProfilePage.jsx
│   │   │   ├── RecommendationsPage.jsx
│   │   │   ├── PlannerPage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── PredictionPage.jsx
│   │   │   ├── AdaptiveQuestionsPage.jsx
│   │   │   └── ChatbotPage.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── auth.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
└── README.md
```

## Backend APIs

Base URL: `http://localhost:5000/api`

### Auth
- `POST /auth/signup`
- `POST /auth/login`

### Student Inputs + AI Engine
- `POST /student/profile` (marks, skills, interests + weak/strong topic detection)
- `GET /student/profile`

### Recommendations
- `GET /recommendations/` (topics + videos + practice questions)

### Study Planner
- `GET /planner/` (daily tasks + weekly tasks)

### Progress Tracking
- `POST /progress/entry`
- `GET /progress/dashboard` (graphs + completion percentage)

### Performance Prediction
- `POST /prediction/`

### Adaptive Difficulty Questions
- `POST /adaptive/questions`

### Chatbot Tutor
- `POST /chatbot/`

## Database Schema (MySQL)

See [DATABASE_SCHEMA.md](backend/DATABASE_SCHEMA.md).

## Setup

### 1) Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

One-click MySQL bootstrap (Windows):

```bash
setup_mysql_db.bat
```

### 2) Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend runs on `http://localhost:5173` and calls backend via `VITE_API_BASE_URL`.

### Local development note

- Run MySQL locally and create the database `ai_study_recommendation`.
- Set `DATABASE_URL` in `backend/.env`, for example:
   `mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation`
- Initialize tables with `python scripts/init_db.py`.

## Key AI Flow

1. Student submits marks, skills, interests.
2. Random Forest classifies strong vs weak topics.
3. Hybrid NLP ranks topic catalog using TF-IDF + BERT similarity.
4. System recommends topics, videos, and practice questions.
5. Planner generates daily/weekly tasks.
6. Dashboard tracks completion and chart data.
7. Random Forest regressor predicts upcoming performance.
8. Adaptive generator produces difficulty-specific questions.
9. GPT tutor answers study queries contextually.

## Deployment for Final Year Project

### Production Setup

1. **Install backend dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start MySQL and initialize tables**:
   ```bash
   cd backend
   python scripts/init_db.py
   ```

3. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   ```

4. **Run Demo**:
   - On Windows: Double-click `run_demo.bat`
   - On Linux/Mac: `chmod +x run_demo.sh && ./run_demo.sh`

5. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000/api

### Production Profile Notes
- Chatbot is disabled in production demo profile (`CHATBOT_ENABLED=false`) to keep deployment self-contained.
- All other report-aligned AI modules remain active.
- Configure strong `SECRET_KEY` and `JWT_SECRET_KEY` in backend `.env` for production runs.

### Note on Tomcat
Tomcat is designed for Java applications and cannot run Python Flask applications. This project uses Python/Flask for the backend, so Tomcat is not applicable. For deployment, use the provided scripts or deploy to cloud platforms like Heroku, AWS, or Azure.

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
