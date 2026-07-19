from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src.schemas.user import UserSchema, UserUpdateSchema
from src.services.user_service import UserService

users_bp = Blueprint("users", __name__)


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user's profile."""
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    schema = UserSchema()
    return jsonify({"success": True, "data": schema.dump(user)})


@users_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_profile():
    """Update current user's profile."""
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    schema = UserUpdateSchema()
    try:
        data = schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user = UserService.update_user(user, data)
    return jsonify({"success": True, "data": UserSchema().dump(user)})
