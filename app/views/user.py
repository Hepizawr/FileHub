import traceback
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user

from app import db
from app.models import User
from app.views.admin import admin_required

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/all', methods=['GET'])
def get_all():
    return jsonify([user.to_dict() for user in User.query.all()])


@user_bp.route('/<string:username>', methods=['GET'])
def get_by_username(username):
    if user := User.query.filter_by(username=username).first():
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_by_id(user_id):
    if user := User.query.filter_by(id=user_id).first():
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


@user_bp.route('/create', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = True if request.form.get('is-admin') else False

    user = User(username=username, is_admin=is_admin)
    user.set_password(password)

    next_url = url_for(request.args.get('next')) if request.args.get('next') else request.referrer

    try:
        db.session.add(user)
        db.session.commit()
        if current_user.is_anonymous:
            login_user(user, remember=True)
        return redirect(next_url)
    except Exception as e:
        db.session.rollback()
        print(e)
        return redirect(request.referrer)


@user_bp.route('/<int:user_id>/update', methods=['POST'])
@admin_required
def update(user_id):
    if user_db := User.query.filter_by(id=user_id).first():
        username = request.form.get('username')
        is_admin = True if request.form.get('is-admin') else False

        user_db.username = username
        user_db.is_admin = is_admin

        try:
            db.session.add(user_db)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

    return redirect(request.referrer)


@user_bp.route('/<int:user_id>/delete', methods=['GET'])
@admin_required
def delete(user_id):
    if user_db := User.query.filter_by(id=user_id).first():
        try:
            db.session.delete(user_db)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()

    return redirect(request.referrer)
