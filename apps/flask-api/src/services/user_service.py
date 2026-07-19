import logging
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions import db
from src.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    """Service layer for user operations."""

    @staticmethod
    def create_user(data: dict[str, Any]) -> User:
        """Create a new user."""
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        logger.info(f"User created: {user.email}")
        return user

    @staticmethod
    def get_by_id(user_id: str) -> User | None:
        """Get user by ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        """Get user by email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        """Authenticate user by email and password."""
        user = UserService.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def update_user(user: User, data: dict[str, Any]) -> User:
        """Update user fields."""
        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> bool:
        """Change user password."""
        if not check_password_hash(user.password_hash, old_password):
            return False
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True
