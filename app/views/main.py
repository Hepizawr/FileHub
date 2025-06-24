from flask import flash, render_template, request
from sqlalchemy import or_

import app.models as db_model
from app.views import index_bp


@index_bp.route("/", methods=["GET"])
@index_bp.route("/<int:page>", methods=["GET"])
def index(page: int = 1):
    if query := request.args.get("query"):
        files = db_model.File.query.filter(
            or_(db_model.File.name.contains(query), db_model.File.format.contains(query))
        ).paginate(page=page, per_page=4)

        flash(f"Search result for '{query}'", "message")
    else:
        files = db_model.File.query.paginate(page=page, per_page=4)

    users = db_model.User.query.all()

    context = {
        "title": "FileHub",
        "users": users,
        "files": files.items,
        "page": files.page,
        "pages": files.pages,
        "has_next": files.has_next,
        "has_prev": files.has_prev,
    }
    return render_template("index.html", **context)
