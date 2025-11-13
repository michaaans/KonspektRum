
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..forms import ProfileEditForm
from ..models.user import User
from ..models.note import Note
from ..models.role import Role


profile = Blueprint('profile', __name__)


@profile.route('/profile/<username>', methods=['GET'])
@login_required
def profile_username(username):
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first()

    if not user:
        abort(404)

    notes_pagination = Note.query.filter_by(users_id=user.id).order_by(Note.created_at.desc()).paginate(
        page=page,
        per_page=3,
        error_out=False
    )

    return render_template('profile/profile.html',
                           user=user,
                           notes=notes_pagination.items,
                           pagination=notes_pagination)


@profile.route('/profile/<username>/edit', methods=['GET', 'POST'])
@login_required
def profile_edit(username):
    # Находим пользователя
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    # Проверяем права доступа
    if user.id != current_user.id and not current_user.is_admin:
        abort(403)

    # Создаем форму
    form = ProfileEditForm(editing_user=user)

    # Для GET запроса заполняем форму текущими данными
    if request.method == 'GET':
        form.full_name.data = user.full_name or ''
        form.username.data = user.username or ''
        form.email.data = user.email or ''
        form.university.data = user.university or ''

        # Заполняем роль только для админов
        if current_user.is_admin:
            form.role_id.data = str(user.role_id) if user.role_id else '3'

    # Для POST запроса - обработка данных
    if form.validate_on_submit():
        try:
            # Обновляем основные поля
            user.full_name = form.full_name.data
            user.username = form.username.data
            user.email = form.email.data
            user.university = form.university.data

            # Обновляем роль если пользователь - админ
            if current_user.is_admin:
                if form.role_id.data:  # Если поле не пустое
                    new_role_id = int(form.role_id.data)

                    # Проверяем, что роль существует
                    role_exists = Role.query.get(new_role_id)
                    if role_exists:
                        user.role_id = new_role_id
                    else:
                        flash(f'Роль с ID {new_role_id} не существует', 'danger')
                        return render_template('profile/edit.html', form=form, user=user)
                else:
                    user.role_id = 3

            # Сохраняем изменения
            db.session.commit()

            flash('Профиль успешно обновлен!', 'success')
            return redirect(url_for('profile.profile_username', username=user.username))

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении профиля', 'danger')
            print(f"ERROR: {str(e)}")

    return render_template('profile/edit.html', form=form, user=user)