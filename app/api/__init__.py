import typing as t
from functools import wraps

import sqlalchemy as sql
from flask import Blueprint, abort
from flask_login import current_user, login_required

api_bp = Blueprint(name="api", url_prefix="/api", import_name=__name__)

import app.api.errors as error

api_bp.register_error_handler(code_or_exception=400, f=error.bad_request)
api_bp.register_error_handler(code_or_exception=403, f=error.access_forbidden)
api_bp.register_error_handler(code_or_exception=403, f=error.item_not_found)
api_bp.register_error_handler(code_or_exception=500, f=error.internal_server_error)

Param = t.ParamSpec("Param")
RetType = t.TypeVar("RetType")


def permission_required(allow_admin: bool = True):
    def wrapper(fn: t.Callable[Param, RetType]) -> t.Callable[Param, RetType]:
        @wraps(fn)
        @login_required
        def decorator(*args: Param.args, **kwargs: Param.kwargs):
            if allow_admin and current_user.is_admin:
                return fn(*args, **kwargs)

            file_id = kwargs["file_id"]
            if Permission.query.filter(
                sql.and_(Permission.user_id == current_user.id, Permission.file_id == file_id)
            ).first():
                return fn(*args, **kwargs)
            return abort(403, description="Access to file is permitted")

        return decorator

    return wrapper


def admin_required():
    def wrapper(fn: t.Callable[Param, RetType]) -> t.Callable[Param, RetType]:
        @wraps(fn)
        @login_required
        def decorator(*args: Param.args, **kwargs: Param.kwargs):
            if not current_user.is_admin:
                return abort(403, description="Admins only!")
            return fn(*args, **kwargs)

        return decorator

    return wrapper


from app.api import files, users
from app.models import Permission
