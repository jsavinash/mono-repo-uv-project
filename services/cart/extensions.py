"""
extensions.py ─ Instantiate all Flask extensions here (no app reference).
Each is initialized later via .init_app(app) inside create_app().
"""

from flask_wtf import CSRFProtect

# db = SQLAlchemy()
# login_manager = LoginManager()
# mail = Mail()
# migrate = Migrate()
csrf = CSRFProtect()
