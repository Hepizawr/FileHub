import os


class Config:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(SCRIPT_DIR, "static")
    TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "templates")
    UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, "storage")

    SECRET_KEY = os.environ.get("SECRET_KEY", "A very secure secret key ")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
