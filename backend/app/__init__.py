import logging
from flask import Flask
from sqlalchemy import text
from .config import get_config
from .extensions import db, bcrypt, jwt, cors


def create_app() -> Flask:
    app = Flask(__name__)
    config = get_config()
    config.validate()
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    with app.app_context():
        db.create_all()

    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )

    from .routes.auth_routes import auth_bp
    from .routes.student_routes import student_bp
    from .routes.recommendation_routes import recommendation_bp
    from .routes.planner_routes import planner_bp
    from .routes.progress_routes import progress_bp
    from .routes.prediction_routes import prediction_bp
    from .routes.adaptive_routes import adaptive_bp
    from .routes.chatbot_routes import chatbot_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(planner_bp, url_prefix="/api/planner")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(prediction_bp, url_prefix="/api/prediction")
    app.register_blueprint(adaptive_bp, url_prefix="/api/adaptive")
    app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}, 200

    @app.get("/api/health/ready")
    def readiness_check():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ready", "database": "connected"}, 200
        except Exception as exc:
            app.logger.warning("Database readiness check failed: %s", exc)
            if app.config.get("DB_REQUIRED", False):
                return {"status": "not_ready", "database": "disconnected"}, 503
            return {
                "status": "ready_with_fallback",
                "database": "disconnected",
                "message": "Running in temporary fallback mode",
            }, 200

    @app.errorhandler(404)
    def not_found(_error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Unhandled server error: %s", error)
        return {"error": "Internal server error"}, 500

    return app
