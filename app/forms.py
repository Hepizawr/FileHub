from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in", render_kw={"class": "dialog-button success"})


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"onchange": "checkUsernameAvailability(this)"},
    )
    password = PasswordField("Password", validators=[DataRequired()])
    is_admin = BooleanField("Admin", default=False)
    submit = SubmitField("Sing up", render_kw={"class": "dialog-button success"})
