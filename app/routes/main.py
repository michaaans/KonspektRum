from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
# from sqlalchemy import desc, asc

from ..models import Note

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():

    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    total_notes_count = Note.query.count()

    if query:

        search_query = Note.fulltext_search(query)
        notes_pagination = search_query.paginate(page=page, per_page=20, error_out=False)

        is_search = True
        search_has_results = notes_pagination.total > 0

    else:

        notes_pagination = Note.query.order_by(Note.created_at.desc()).paginate(
            page=page,
            per_page=20,
            error_out=False
        )

        is_search = False
        search_has_results = False

    return render_template(
        'main/index.html',
        notes=notes_pagination.items,
        pagination=notes_pagination,
        search_query=query,
        total_notes_count=total_notes_count,
        is_search=is_search,
        search_has_results=search_has_results
    )


