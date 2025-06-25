import uuid

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id: str) -> User:
    user_id = uuid.UUID(user_id)
    return User.query.filter_by(id=user_id).first()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User).filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect(url_for("main.index"))
        return redirect(url_for("auth.login"))

    else:
        context = {
            "title": "Log in",
            "form": form,
        }
        return render_template("auth/login.html", **context)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_user = User(id=uuid.uuid4(), username=form.username.data)
            new_user.set_password(form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

            login_user(new_user, remember=True)
            return redirect(url_for("main.index"))
        return redirect(url_for("auth.register"))

    else:
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
