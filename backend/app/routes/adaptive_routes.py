from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.student_profile_model import StudentProfileModel
from ..services.question_service import QuestionService

adaptive_bp = Blueprint("adaptive", __name__)


@adaptive_bp.post("/questions")
@jwt_required()
def generate_adaptive_questions():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    topic = data.get("topic", "General Topic")

    performance_input = data.get("performance_score")
    performance_score = None

    try:
        if performance_input is not None and str(performance_input).strip() != "":
            performance_score = float(performance_input)
    except (TypeError, ValueError):
        performance_score = None

    if performance_score is None:
        profile = StudentProfileModel.get_profile(user_id) or {}
        marks = profile.get("marks", {})

        matched_mark = None
        topic_normalized = str(topic).strip().lower()
        for subject_name, mark in marks.items():
            subject_normalized = str(subject_name).strip().lower()
            if (
                topic_normalized == subject_normalized
                or topic_normalized in subject_normalized
                or subject_normalized in topic_normalized
            ):
                matched_mark = mark
                break

        try:
            performance_score = float(matched_mark) if matched_mark is not None else 60.0
        except (TypeError, ValueError):
            performance_score = 60.0

    performance_score = max(0.0, min(100.0, performance_score))

    result = QuestionService.generate(topic, performance_score)
    return result, 200
