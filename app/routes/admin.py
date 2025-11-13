from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from ..middlewares import admin_required

from ..models import User

admin = Blueprint('admin', __name__)


@admin.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():

    return render_template('admin/admin.html')


