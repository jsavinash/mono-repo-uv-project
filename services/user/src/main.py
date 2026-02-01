import os
from typer import Typer
from flask import Flask
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix
from user.src.extensions import db, debug_toolbar, flask_static_digest
import user.src.config.settings as settings
from user.src.user.views import user_pb


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, static_folder="../public", static_url_path="")

    app.config.from_object(settings)

    if settings_override:
        app.config.update(settings_override)

    middleware(app)

    app.register_blueprint(user_pb)
    # app.register_blueprint(page)

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    flask_static_digest.init_app(app)

    return None


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Enable the Flask interactive debugger in the brower for development.
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    # Set the real IP address into request.remote_addr when behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


command_app = Typer(add_completion=False)


@command_app.command()
def main():
    application = create_app()
    application.run(debug=True)


if __name__ == "__main__":  # pragma: no cover
    command_app()
