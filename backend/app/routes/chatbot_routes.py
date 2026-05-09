from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from ..services.chatbot_service import ChatbotService

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.post("/")
@jwt_required()
def chat():
    if not current_app.config.get("CHATBOT_ENABLED", True):
        return {
            "error": "Tutor chatbot is disabled for this deployment profile"
        }, 503

    payload = request.get_json() or {}
    message = payload.get("message", "")
    student_context = payload.get("student_context", {})

    if not message:
        return {"error": "message is required"}, 400

    response = ChatbotService.ask_tutor(message, student_context)
    return response, 200
