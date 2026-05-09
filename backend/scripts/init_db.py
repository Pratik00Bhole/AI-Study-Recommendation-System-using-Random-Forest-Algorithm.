import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app
from app.extensions import db


def init_db() -> None:
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
        except Exception as exc:
            raise SystemExit(
                "Database initialization failed. Ensure MySQL is running and DATABASE_URL is set correctly. "
                f"Details: {exc}"
            )

        print("Database initialized successfully")


if __name__ == "__main__":
    init_db()
