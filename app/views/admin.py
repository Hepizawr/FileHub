import click
from flask import Blueprint, current_app, render_template

import app.models as db_model
from app import db
from app.api import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.cli.command("createsuperuser")
def createsuperuser():
    username = click.prompt("Username", type=str)
    password = click.prompt("Password", type=str)

    admin = db_model.User(username=username, is_admin=True)
    admin.set_password(password)

    with current_app.app_context():
        try:
            db.session.add(admin)
            db.session.commit()
            click.echo("Superuser created successfully.")
        except Exception as e:
            db.session.rollback()
            click.echo(f"Error creating superuser: {e}")


@admin_bp.route("/")
@admin_bp.route("/files")
@admin_bp.route("/files/<int:page>")
@admin_required()
def files(page=1):
    files = db_model.File.query.paginate(page=page, per_page=4)
    users = db_model.User.query.all()

    context = {
        "title": "Admin",
        "users": users,
        "files": files.items,
        "page": files.page,
        "pages": files.pages,
        "has_next": files.has_next,
        "has_prev": files.has_prev,
    }
    return render_template("admin/files.html", **context)


@admin_bp.route("/users")
@admin_bp.route("/users/<int:page>")
@admin_required()
def users(page: int = 1):
    users = db_model.User.query.paginate(page=page, per_page=4)

    context = {
        "title": "Admin",
        "users": users.items,
        "page": users.page,
        "pages": users.pages,
        "has_next": users.has_next,
        "has_prev": users.has_prev,
    }
    return render_template("admin/users.html", **context)


@admin_bp.route("/logs")
@admin_bp.route("/logs/<int:page>")
@admin_required()
def logs(page: int = 1):
    logs = db_model.Download.query.order_by(db_model.Download.timestamp.desc()).paginate(page=page, per_page=4)

    context = {
        "title": "Admin",
        "logs": logs.items,
        "page": logs.page,
        "pages": logs.pages,
        "has_next": logs.has_next,
        "has_prev": logs.has_prev,
    }
    return render_template("admin/logs.html", **context)
