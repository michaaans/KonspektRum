from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
# from sqlalchemy import desc, asc

from ..models import Note

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():

    page = request.args.get('page', 1, type=int)

    notes_pagination = Note.query.order_by(Note.created_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    return render_template('main/index.html', notes=notes_pagination.items, pagination=notes_pagination)


@main.route('/search', methods=['GET'])
@login_required
def search():

    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    if not query:
        return render_template('main/search.html',
                               search_notes=[],
                               search_query='',
                               pagination=None)

    search_query = Note.fulltext_search(query)

    pagination = search_query.paginate(page=page, per_page=20, error_out=False)

    return render_template('main/search.html', search_notes=pagination.items, search_query=query, pagination=pagination)
