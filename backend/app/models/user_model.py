from datetime import datetime
from sqlalchemy import func
from ..extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    standard = db.Column(db.Integer, nullable=False, default=10)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class UserModel:
    @staticmethod
    def _to_record(user: User | None):
        if not user:
            return None
        return {
            "_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "standard": int(user.standard),
            "password": user.password,
            "created_at": user.created_at,
        }

    @staticmethod
    def create_user(data: dict) -> str:
        user = User(
            name=data["name"],
            email=str(data["email"]).lower(),
            standard=int(data.get("standard", 10)),
            password=data["password"],
        )
        db.session.add(user)
        db.session.commit()
        return str(user.id)

    @staticmethod
    def get_by_email(email: str):
        normalized_email = str(email).lower().strip()
        user = User.query.filter(func.lower(User.email) == normalized_email).first()
        return UserModel._to_record(user)

    @staticmethod
    def get_by_id(user_id: str):
        try:
            numeric_id = int(user_id)
        except (TypeError, ValueError):
            return None
        user = db.session.get(User, numeric_id)
        return UserModel._to_record(user)
