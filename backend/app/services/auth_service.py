from ..extensions import bcrypt
from ..models.user_model import UserModel


class AuthService:
    @staticmethod
    def signup(name: str, email: str, standard: str, password: str):
        existing = UserModel.get_by_email(email)
        if existing:
            return None, None, "Email already exists"

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            user_id = UserModel.create_user({"name": name, "email": email, "standard": standard, "password": hashed})
        except RuntimeError:
            return None, None, "Database is unavailable. Please try again after backend is online."
        return user_id, standard, None

    @staticmethod
    def login(email: str, password: str):
        user = UserModel.get_by_email(email)
        if not user:
            return None

        if not bcrypt.check_password_hash(user["password"], password):
            return None

        return user
