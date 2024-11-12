import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "A very secure secret key ")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
