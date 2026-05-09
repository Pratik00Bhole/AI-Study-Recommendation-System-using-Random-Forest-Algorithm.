from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.student_profile_model import StudentProfileModel
from ..models.progress_model import ProgressModel
from ..services.ai_engine_service import AIEngineService
from ..services.recommendation_service import RecommendationService
from ..services.planner_service import PlannerService

planner_bp = Blueprint("planner", __name__)


@planner_bp.get("/")
@jwt_required()
def generate_plan():
    user_id = get_jwt_identity()
    profile = StudentProfileModel.get_profile(user_id)
    if not profile:
        return {"error": "Student profile not found"}, 404

    analysis = AIEngineService.detect_topic_strengths(
        marks=profile.get("marks", {}),
        skills=profile.get("skills", []),
        interests=profile.get("interests", []),
        subject_levels=profile.get("subject_levels", {}),
    )
    progress_entries = ProgressModel.list_entries(user_id)

    recommendations = RecommendationService.recommend(
        weak_topics=analysis["weak_topics"],
        skills=profile.get("skills", []),
        interests=profile.get("interests", []),
        top_k=4,
        marks=profile.get("marks", {}),
        subject_levels=profile.get("subject_levels", {}),
        progress_entries=progress_entries,
    )

    plan = PlannerService.create_daily_weekly_plan(
        recommended_topics=recommendations,
        profile=profile,
        analysis=analysis,
        progress_entries=progress_entries,
    )
    return {
        "daily_tasks": plan["daily_tasks"],
        "weekly_tasks": plan["weekly_tasks"],
    }, 200
