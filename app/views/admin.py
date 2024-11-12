from functools import wraps

import click
from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, url_for, current_app, jsonify, send_file, render_template

from app import db
from app.models import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.cli.command('createsuperuser')
def createsuperuser():
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)

    admin = User(username=username, is_admin=True)
    admin.set_password(password)

    with current_app.app_context():
        try:
            db.session.add(admin)
            db.session.commit()
            click.echo('Superuser created successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f"Error creating superuser: {e}")


@admin_bp.route('/')
@admin_bp.route('/files')
@admin_bp.route('/files/<int:page>')
@admin_required
def files(page=1):
    files = File.query.paginate(page=page, per_page=4)
    users = User.query.all()

    context = {
        'title': 'Admin',
        'users': users,
        'files': files.items,
        'page': files.page,
        'pages': files.pages,
        'has_next': files.has_next,
        'has_prev': files.has_prev,
    }
    return render_template('admin/files.html', **context)


@admin_bp.route('/users')
@admin_bp.route('/users/<int:page>')
@admin_required
def users(page=1):
    users = User.query.paginate(page=page, per_page=4)

    context = {
        'title': 'Admin',
        'users': users.items,
        'page': users.page,
        'pages': users.pages,
        'has_next': users.has_next,
        'has_prev': users.has_prev,
    }
    return render_template('admin/users.html', **context)


@admin_bp.route('/logs')
@admin_bp.route('/logs/<int:page>')
@admin_required
def logs(page=1):
    logs = Download.query.order_by(Download.timestamp.desc()).paginate(page=page, per_page=4)

    context = {
        'title': 'Admin',
        'logs': logs.items,
        'page': logs.page,
        'pages': logs.pages,
        'has_next': logs.has_next,
        'has_prev': logs.has_prev,
    }
    return render_template('admin/logs.html', **context)
