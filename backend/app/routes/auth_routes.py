from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup():
    data = request.get_json() or {}
    required_fields = ["name", "email", "standard", "password"]
    if any(field not in data for field in required_fields):
        return {"error": "name, email, standard, and password are required"}, 400

    user_id, standard, error = AuthService.signup(
        data["name"], data["email"], data["standard"], data["password"]
    )
    if error:
        status_code = 503 if "Database is unavailable" in error else 409
        return {"error": error}, status_code

    token = create_access_token(identity=user_id)
    return {
        "message": "Signup successful",
        "token": token,
        "user": {
            "id": user_id,
            "name": data["name"],
            "email": data["email"].lower(),
            "standard": standard,
        },
    }, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "email and password are required"}, 400

    user = AuthService.login(email, password)
    if not user:
        return {"error": "Invalid credentials"}, 401

    user_id = str(user["_id"])
    token = create_access_token(identity=user_id)
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user_id,
            "name": user.get("name"),
            "email": user.get("email"),
            "standard": int(user.get("standard", 10)),
        },
    }, 200


@auth_bp.get("/validate")
@jwt_required()
def validate_token():
    return {"status": "valid", "user_id": get_jwt_identity()}, 200
