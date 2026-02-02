"""
extensions.py ─ Instantiate all Flask extensions here (no app reference).
Each is initialized later via .init_app(app) inside create_app().
"""

from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

#db = SQLAlchemy()
#login_manager = LoginManager()
#mail = Mail()
#migrate = Migrate()
csrf = CSRFProtect()
