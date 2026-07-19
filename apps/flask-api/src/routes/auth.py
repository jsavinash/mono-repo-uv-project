from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError

from src.extensions import db, limiter
from src.models.token_blacklist import TokenBlacklist
from src.schemas.user import ChangePasswordSchema, LoginSchema, UserCreateSchema
from src.services.user_service import UserService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5/minute")
def register():
    """Register a new user."""
    schema = UserCreateSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    # Check if user already exists
    if UserService.get_by_email(data["email"]):
        return jsonify(
            {"success": False, "errors": {"email": "Email already registered."}}
        ), 409

    if UserService.get_by_email(data["username"]):
        return jsonify(
            {"success": False, "errors": {"username": "Username already taken."}}
        ), 409

    user = UserService.create_user(data)
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify(
        {
            "success": True,
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    ), 201


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def login():
    """Authenticate user and return JWT tokens."""
    schema = LoginSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user = UserService.authenticate(data["email"], data["password"])
    if not user:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify(
        {
            "success": True,
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"success": True, "access_token": access_token})


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout user by blacklisting the token."""
    jti = get_jwt()["jti"]
    token_type = get_jwt()["type"]
    user_id = get_jwt_identity()
    expires = get_jwt()["exp"]

    from datetime import datetime, timezone

    blacklisted = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires_at=datetime.fromtimestamp(expires, tz=timezone.utc),
    )
    db.session.add(blacklisted)
    db.session.commit()

    return jsonify({"success": True, "message": "Successfully logged out."})


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """Change current user's password."""
    schema = ChangePasswordSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    if not UserService.change_password(
        user, data["old_password"], data["new_password"]
    ):
        return jsonify(
            {"success": False, "errors": {"old_password": "Wrong password."}}
        ), 400

    return jsonify({"success": True, "message": "Password updated successfully."})
