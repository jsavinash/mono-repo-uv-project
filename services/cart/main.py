"""
__init__.py ─ Application factory.
Call  create_app()  to get a fully-wired Flask instance.
"""

import os

from flask import Flask
from typer import Typer

from cart.config import config_map
from cart.extensions import csrf

# from cart.extensions import csrf, db, login_manager, mail, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Factory that builds and returns the Flask application."""

    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    # ─── Extensions ─────────────────────────────────────────
    # db.init_app(app)
    # migrate.init_app(app, db)
    # login_manager.init_app(app)
    # mail.init_app(app)
    csrf.init_app(app)

    # login_manager.login_view = "auth.login"
    # login_manager.login_message = "Please log in to access this page."
    # login_manager.login_message_category = "warning"

    # ─── User loader (flask-login) ──────────────────────────
    # @login_manager.user_loader
    # def load_user(user_id: str):
    #     from app.models.user import User

    #     return db.session.get(User, int(user_id))

    # ─── Blueprints ─────────────────────────────────────────
    # from cart.routes.auth import auth_bp
    # from cart.routes.cart import cart_bp
    # from cart.routes.main import main_bp
    # from cart.routes.orders import orders_bp
    # from cart.routes.products import products_bp

    # app.register_blueprint(main_bp)
    # app.register_blueprint(auth_bp, url_prefix="/auth")
    # app.register_blueprint(products_bp, url_prefix="/products")
    # app.register_blueprint(cart_bp, url_prefix="/cart")
    # app.register_blueprint(orders_bp, url_prefix="/orders")

    # ─── Seed on first run ──────────────────────────────────
    # with app.app_context():
    #     from app.seed import seed_db

    #     db.create_all()
    #     seed_db()

    return app


execute = Typer(add_completion=False)


@execute.command()
def main() -> None:
    """Run Flask App."""
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    execute()
