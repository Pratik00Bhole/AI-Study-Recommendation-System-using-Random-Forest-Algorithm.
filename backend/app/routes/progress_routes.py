from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.progress_model import ProgressModel
from ..services.progress_service import ProgressService
from ..utils.serializers import serialize_doc

progress_bp = Blueprint("progress", __name__)


@progress_bp.post("/entry")
@jwt_required()
def add_progress_entry():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    ProgressModel.create_progress_entry(user_id, data)
    return {"message": "Progress entry added"}, 201


@progress_bp.get("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    entries = [serialize_doc(item) for item in ProgressModel.list_entries(user_id)]
    dashboard_data = ProgressService.build_dashboard(entries)
    return {"entries": entries, "dashboard": dashboard_data}, 200
