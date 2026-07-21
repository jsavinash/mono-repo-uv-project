"""
Flask application factory for flask-api.
"""

import logging
import logging.handlers  # needed for RotatingFileHandler
import os
from pathlib import Path

from flask import Flask

from src.config import config_map
from src.extensions import cors, db, jwt, limiter, ma, mail, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    # --- Initialize Extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)
    mail.init_app(app)
    limiter.init_app(app)

    # --- Setup Logging ---
    _setup_logging(app)

    # --- Register Blueprints ---
    _register_blueprints(app)

    # --- Error Handlers ---
    _register_error_handlers(app)

    # --- Shell Context ---
    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

    return app


def _setup_logging(app: Flask) -> None:
    """Configure application logging."""
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))
    log_file = app.config.get("LOG_FILE")

    handlers = [logging.StreamHandler()]
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(
            logging.handlers.RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=5
            )
        )

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
    )


def _register_blueprints(app: Flask) -> None:
    """Register all API blueprints."""
    from src.routes.auth import auth_bp
    from src.routes.health import health_bp
    from src.routes.users import users_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")


def _register_error_handlers(app: Flask) -> None:
    """Register custom error handlers."""

    @app.errorhandler(400)
    def bad_request(error):
        return {"success": False, "message": "Bad request.", "errors": str(error)}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {"success": False, "message": "Authentication required."}, 401

    @app.errorhandler(403)
    def forbidden(error):
        return {"success": False, "message": "Forbidden."}, 403

    @app.errorhandler(404)
    def not_found(error):
        return {"success": False, "message": "Resource not found."}, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"success": False, "message": "Method not allowed."}, 405

    @app.errorhandler(429)
    def too_many_requests(error):
        return {
            "success": False,
            "message": "Too many requests. Please try again later.",
        }, 429

    @app.errorhandler(500)
    def internal_error(error):
        return {"success": False, "message": "Internal server error."}, 500
