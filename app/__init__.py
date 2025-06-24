from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config as app_config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder=app_config.STATIC_DIR,
        template_folder=app_config.TEMPLATE_DIR,
    )
    app.config.from_object(app_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from app import api, models, views

        app.register_blueprint(views.index_bp)
        app.register_blueprint(views.auth.auth_bp)
        app.register_blueprint(views.admin.admin_bp)
        app.register_blueprint(api.api_bp)

    return app
