import uuid

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return db.session.query(User).get(uuid.UUID(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User).filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect(url_for("main.index"))

    else:
        context = {
            "title": "Log in",
            "form": form,
        }
        return render_template("auth/login.html", **context)


@auth_bp.route("/register", methods=["GET"])
def register():
    form = RegisterForm()
    context = {
        "title": "Sign up",
        "form": form,
    }

    return render_template("auth/singup.html", **context)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
