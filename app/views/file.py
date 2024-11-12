import os
import traceback

from flask import Blueprint, request, redirect, url_for, current_app, jsonify, send_file, flash
from flask_login import login_required, current_user
from app import db
from app.models import *
from app.views.admin import admin_required

file_bp = Blueprint('file', __name__, url_prefix='/file')


@file_bp.route('/create', methods=['POST'])
@admin_required
def create():
    if file := request.files.get('file'):
        file_name = request.form.get('file_name') or file.filename
        file_allowed_users = request.form.get('allowed-users').split(', ')
        file_format = "." + file.filename.split('.')[-1]
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save('app/' + file_path)

        file = File(name=file_name, format=file_format, url=file_path)
        file.users = [user for username in file_allowed_users if
                      (user := User.query.filter_by(username=username).first())]

        try:
            db.session.add(file)
            db.session.commit()
            return redirect(request.referrer)
        except Exception as e:
            db.session.rollback()
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)


@file_bp.route('/<int:file_id>', methods=['GET'])
def get_by_id(file_id):
    if file := File.query.filter_by(id=file_id).first():
        return jsonify(file.to_dict())
    return jsonify({'error': 'File not found'}), 404


@file_bp.route('/<int:file_id>/update', methods=['POST'])
@admin_required
def update(file_id):
    if file_db := File.query.filter_by(id=file_id).first():
        file_name = request.form.get('file_name')
        file_allowed_users = request.form.get('allowed-users').split(', ')

        file_db.name = file_name
        file_db.users = [user for username in file_allowed_users if
                         (user := User.query.filter_by(username=username).first())]

        if file := request.files.get('file'):
            if os.path.exists(os.path.join('app', file_db.url)):
                os.remove(os.path.join('app', file_db.url))
            file_format = "." + file.filename.split('.')[-1]
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save('app/' + file_path)
            file_db.format = file_format
            file_db.url = file_path

        try:
            db.session.add(file_db)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()

    return redirect(request.referrer)


@file_bp.route('/<int:file_id>/delete', methods=['GET'])
@admin_required
def delete(file_id):
    if file_db := File.query.filter_by(id=file_id).first():
        try:
            if os.path.exists(os.path.join('app', file_db.url)):
                os.remove(os.path.join('app', file_db.url))

            db.session.delete(file_db)
            db.session.commit()

        except Exception as e:
            traceback.print_exc()
            db.session.rollback()

    return redirect(request.referrer)


@file_bp.route('/<int:file_id>/download', methods=['GET'])
@login_required
def download(file_id):
    if file := File.query.filter_by(id=file_id).first():
        if file.users and (not current_user.is_admin) and (current_user not in file.users):
            flash('Administration restricted access to this file', category="error")
            return redirect(request.referrer)

        try:
            file.downloads.append(Download(user_id=current_user.id, file_id=file.id))
            db.session.add(file)
            db.session.commit()
            return send_file(file.url, as_attachment=True, download_name=f"{file.name}{file.format}")
        except Exception as e:
            db.session.rollback()
            print(e)
