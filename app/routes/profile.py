
from flask import Blueprint, render_template
from flask_login import login_required

from ..models.user import User
from ..models.note import Note

profile = Blueprint('profile', __name__)


@profile.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile_username(username):

    user = User.query.filter_by(username=username).first()

    notes = Note.query.filter_by(users_id=user.id).all()

    return render_template('profile/profile.html', user=user, notes=notes)


