from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.student_profile_model import StudentProfileModel
from ..services.ai_engine_service import AIEngineService
from ..utils.serializers import serialize_doc

student_bp = Blueprint("student", __name__)


@student_bp.post("/profile")
@jwt_required()
def save_student_profile():
    user_id = get_jwt_identity()
    payload = request.get_json() or {}

    student_details = payload.get("student_details", {})
    subjects = payload.get("subjects", [])
    skills = payload.get("skills", [])
    interests = payload.get("interests", [])

    marks = payload.get("marks", {})
    subject_levels = payload.get("subject_levels", {})

    if isinstance(subjects, list) and subjects:
        normalized_marks = {}
        normalized_levels = {}
        cleaned_subjects = []

        for item in subjects:
            if not isinstance(item, dict):
                continue

            name = str(item.get("name", "")).strip()
            if not name:
                continue

            level = str(item.get("level", "average")).strip().lower() or "average"
            if level not in {"good", "average", "low"}:
                level = "average"

            try:
                mark = float(item.get("marks", 0))
            except (TypeError, ValueError):
                mark = 0.0

            mark = max(0.0, min(100.0, mark))
            normalized_marks[name] = mark
            normalized_levels[name] = level
            cleaned_subjects.append({"name": name, "level": level, "marks": mark})

        marks = normalized_marks
        subject_levels = normalized_levels
        subjects = cleaned_subjects

    StudentProfileModel.upsert_profile(
        user_id,
        {
            "student_details": student_details,
            "subjects": subjects,
            "marks": marks,
            "subject_levels": subject_levels,
            "skills": skills,
            "interests": interests,
        },
    )

    analysis = AIEngineService.detect_topic_strengths(marks, skills, interests, subject_levels)
    return {"message": "Profile saved", "analysis": analysis}, 200


@student_bp.get("/profile")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = StudentProfileModel.get_profile(user_id)
    return {"profile": serialize_doc(profile)}, 200
