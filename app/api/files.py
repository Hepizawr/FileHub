import os
import uuid

from flask import current_app, jsonify, request, send_file
from flask_login import current_user

import app.models as db_model
from app import db, utils
from app.api import admin_required, api_bp, permission_required


@api_bp.route("/files", methods=["GET"])
def get_files():
    files = db_model.File.query.all()
    return jsonify([utils.convert_db_model_to_dict(file) for file in files]), 200


@api_bp.route("/files/<uuid:file_id>", methods=["GET"])
def get_file_by_id(file_id):
    if file := db_model.File.query.filter_by(id=file_id).first():
        return jsonify(utils.convert_db_model_to_dict(file)), 200
    return jsonify({"message": "File not found"}), 404


@api_bp.route("/files", methods=["POST"])
@admin_required()
def create_file():
    if not (file := request.files.get("file")):
        return jsonify({"message": "No file part"}), 400
    data = {}
    data["id"] = uuid.uuid4()
    data["name"] = request.form.get("file_name", file.filename)
    data["format"] = "." + file.filename.split(".")[-1]
    data["users"] = request.form.get("allowed-users").split(", ")
    utils.save_file(file=file, directory=current_app.config["UPLOAD_FOLDER"], name=str(data["id"]))
    return utils.create_db_record_as_response(db_type=db_model.File, data=data)


@api_bp.route("/files/<uuid:file_id>", methods=["PATCH"])
@admin_required()
def update_file(file_id):
    if not (file_db := db_model.File.query.filter_by(id=file_id).first()):
        return jsonify({"message": "File not found"}), 404
    new_data = {}
    new_data["name"] = request.form.get("file_name", file_db.name)
    new_data["users"] = request.form.get("allowed-users").split(", ")
    if file := request.files.get("file"):
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_db.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        new_data["format"] = "." + file.filename.split(".")[-1]
        utils.save_file(
            file=file,
            directory=current_app.config["UPLOAD_FOLDER"],
            name=str(file_db.id),
        )
    return utils.update_db_record_as_response(db_model=file_db, new_data=new_data)


@api_bp.route("/files/<uuid:file_id>", methods=["DELETE"])
@admin_required()
def delete_file(file_id):
    if not (file_db := db_model.File.query.filter_by(id=file_id).first()):
        return jsonify({"message": "File not found"}), 404
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_db.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return utils.delete_db_record_as_response(db_model=file_db)


@api_bp.route("/files/<uuid:file_id>/download", methods=["GET"])
@permission_required()
def download_file(file_id):
    if not (file_db := db_model.File.query.filter_by(id=file_id).first()):
        return jsonify({"message": "File not found"}), 404
    try:
        file_db.downloads.append(db_model.Download(user_id=current_user.id, file_id=file_db.id))
        db.session.commit()
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_db.filename)
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{file_db.name}{file_db.format}",
        )
    except Exception as e:
        db.session.rollback()
        print(e)
