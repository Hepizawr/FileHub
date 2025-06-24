from flask import jsonify, request
from flask_login import login_required
from werkzeug.security import generate_password_hash

import app.models as db_model
from app import utils
from app.api import admin_required, api_bp


@api_bp.route("/users", methods=["GET"])
@admin_required()
def get_users():
    users = db_model.User.query.all()
    return jsonify([utils.convert_db_model_to_dict(user) for user in users]), 200


@api_bp.route("/users/<uuid:user_id>", methods=["GET"])
@admin_required()
def get_user_by_id(user_id):
    if not (user := db_model.User.query.filter_by(id=user_id).first()):
        return jsonify({"message": "User not found"}), 404
    return jsonify(utils.convert_db_model_to_dict(user)), 200


@api_bp.route("/users/<string:username>", methods=["GET"])
@admin_required()
def get_user_by_username(username):
    if not (user := db_model.User.query.filter_by(username=username).first()):
        return jsonify({"message": "User not found"}), 404
    return jsonify(utils.convert_db_model_to_dict(user)), 200


@api_bp.route("/users", methods=["POST"])
def create_user():
    data = request.form.to_dict()
    if db_model.User.query.filter_by(username=data["username"]).first():
        response_data = jsonify({"message": "User with this username already exists"})
        return jsonify(response_data), 400
    data["password_hash"] = generate_password_hash(data["password"])
    return utils.create_db_record_as_response(db_type=db_model.User, data=data)


@api_bp.route("/users/<uuid:user_id>", methods=["PATCH"])
@login_required
def update_user(user_id):
    data = request.form.to_dict()
    if not (user := db_model.User.query.filter_by(id=user_id).first()):
        return jsonify({"message": "User not found"}), 404
    return utils.update_db_record_as_response(db_model=user, new_data=data)


@api_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
@admin_required()
def delete_user(user_id):
    if not (user := db_model.User.query.filter_by(id=user_id).first()):
        return jsonify({"message": "User not found"}), 404
    return utils.delete_db_record_as_response(db_model=user)
