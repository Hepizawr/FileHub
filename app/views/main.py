from flask import Blueprint, render_template, request, flash
from sqlalchemy import or_
from app.models import *

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/<int:page>')
def index(page=1):
    if query := request.args.get('query'):
        files = File.query.filter(
            or_(
                File.name.contains(query),
                File.format.contains(query)
            )
        ).paginate(page=page, per_page=4)

        flash(f"Search result for '{query}'", "message")
    else:
        files = File.query.paginate(page=page, per_page=4)

    users = User.query.all()

    context = {
        'title': 'FileHub',
        'users': users,
        'files': files.items,
        'page': files.page,
        'pages': files.pages,
        'has_next': files.has_next,
        'has_prev': files.has_prev,
    }
    return render_template('index.html', **context)
