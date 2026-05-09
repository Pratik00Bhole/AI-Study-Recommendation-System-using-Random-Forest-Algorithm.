from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.prediction_service import PredictionService

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.post("/")
@jwt_required()
def predict_performance():
    payload = request.get_json() or {}

    avg_mark = float(payload.get("avg_mark", 0))
    completed_tasks = int(payload.get("completed_tasks", 0))
    consistency_score = float(payload.get("consistency_score", 0))

    score = PredictionService.predict(avg_mark, completed_tasks, consistency_score)
    return {
        "predicted_score": score,
        "prediction_band": "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Improvement",
    }, 200
