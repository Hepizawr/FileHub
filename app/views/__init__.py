from flask import Blueprint

index_bp = Blueprint(name="main", import_name=__name__)

from app.views import admin, auth, main
