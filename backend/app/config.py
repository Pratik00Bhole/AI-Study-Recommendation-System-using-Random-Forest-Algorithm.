import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _as_list(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _env_name() -> str:
    return os.getenv("FLASK_ENV", "development").strip().lower()


class Config:
    ENV_NAME = _env_name()
    DEBUG = _as_bool(os.getenv("FLASK_DEBUG"), default=ENV_NAME == "development")

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        days=_as_int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_DAYS"), 30)
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }
    CORS_ORIGINS = _as_list(
        os.getenv("CORS_ORIGINS"),
        [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5500",
        ],
    )

    CHATBOT_ENABLED = _as_bool(
        os.getenv("CHATBOT_ENABLED"), default=ENV_NAME != "production"
    )
    DB_REQUIRED = _as_bool(os.getenv("DB_REQUIRED"), default=ENV_NAME == "production")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @classmethod
    def validate(cls):
        if cls.ENV_NAME == "production":
            if cls.SECRET_KEY in {"", "dev-secret"}:
                raise ValueError("SECRET_KEY must be set to a strong value in production")
            if cls.JWT_SECRET_KEY in {"", "dev-jwt-secret"}:
                raise ValueError("JWT_SECRET_KEY must be set to a strong value in production")


def get_config():
    return Config
