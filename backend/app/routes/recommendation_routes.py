from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.student_profile_model import StudentProfileModel
from ..models.progress_model import ProgressModel
from ..services.ai_engine_service import AIEngineService
from ..services.recommendation_service import RecommendationService

recommendation_bp = Blueprint("recommendations", __name__)


@recommendation_bp.get("/")
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()
    profile = StudentProfileModel.get_profile(user_id)
    if not profile:
        return {"error": "Student profile not found"}, 404

    marks = profile.get("marks", {})
    skills = profile.get("skills", [])
    interests = profile.get("interests", [])
    subject_levels = profile.get("subject_levels", {})
    progress_entries = ProgressModel.list_entries(user_id)

    analysis = AIEngineService.detect_topic_strengths(marks, skills, interests, subject_levels)
    recommendations = RecommendationService.recommend(
        weak_topics=analysis["weak_topics"],
        skills=skills,
        interests=interests,
        top_k=5,
        marks=marks,
        subject_levels=subject_levels,
        progress_entries=progress_entries,
    )

    return {
        "analysis": analysis,
        "recommendations": recommendations,
    }, 200
