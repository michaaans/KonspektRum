
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from ..models.user import User
from ..forms import RegistrationForm, LoginForm
from ..extensions import db

auth = Blueprint('auth', __name__)


@auth.route('/auth/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():

        random_avatar = User.get_random_avatar()

        user = User(username=form.username.data, full_name=form.full_name.data,
                    email=form.email.data, university=form.university.data, role_id=3, avatar=random_avatar)

        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Ошибка при регистрации :( ', 'danger')
            print(str(e))

    return render_template('auth/registration.html', form=form)


@auth.route('/auth/login', methods=['GET','POST' ])
def login():

    form = LoginForm()

    next_page = request.args.get('next')
    print(f"Next parameter from URL: {next_page}")

    if next_page:
        form.next.data = next_page
        print(f"Next parameter set in form: {form.next.data}")

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)

            next_page = form.next.data
            print(f"Next page from form after submit: {next_page}")

            # Отладочная информация
            # print(f"Next page: {next_page}")

            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')

            flash('Авторизация прошла успешно', 'success')
            return redirect(next_page)

        flash('Ошибка при авторизации :( Проверьте логин или пароль', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/auth/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'warning')
    return redirect(url_for('main.index'))
