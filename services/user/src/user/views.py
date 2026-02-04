from flask import Blueprint, jsonify, make_response, request

from user.src.extensions import db
from user.src.models.user import User

user_pb = Blueprint(
    "user", __name__, template_folder="templates", url_prefix="/api/v1/users"
)


@user_pb.route("/test", methods=["GET"])
def test():
    return make_response(jsonify({"message": "test route"}), 200)


# get all users
@user_pb.route("/", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except:
        return make_response(jsonify({"message": "error getting users"}), 500)


# create a user
@user_pb.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data["username"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "user created"}), 201)
    except:
        return make_response(jsonify({"message": "error creating user"}), 500)


# get a user by id
@user_pb.route("/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error getting user"}), 500)


# update a user
@user_pb.route("/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data["username"]
            user.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": "user updated"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error updating user"}), 500)


# delete a user
@user_pb.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "user deleted"}), 200)
        return make_response(jsonify({"message": "user not found"}), 404)
    except:
        return make_response(jsonify({"message": "error deleting user"}), 500)
