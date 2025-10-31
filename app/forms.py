from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from .models.user import User


class RegistrationForm(FlaskForm):
    # Личная информация
    full_name = StringField('ФИО', validators=[
        DataRequired(message='Поле ФИО обязательно для заполнения'),
        Length(min=5, max=100, message='ФИО должно быть от 5 до 100 символов')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "Иванов Иван Иванович"
    })

    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Имя пользователя обязательно для заполнения'),
        Length(min=3, max=64, message='Имя пользователя должно быть от 3 до 64 символов'),
        Regexp('^[A-Za-z0-9_]+$', message='Неправильно указан логин')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "_username228_",
        "pattern": "[A-Za-z0-9_]+",
        "title": "Только английские буквы, цифры и символ _"
    })

    email = StringField('Email', validators=[
        DataRequired(message='Email обязателен'),
        Email(message='Введите корректный email адрес'),
        Length(max=120, message='Email не должен превышать 120 символов')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "example@email.com",
        "type": "email"
    })

    # Учебная информация
    university = StringField('ВУЗ', validators=[
        DataRequired(message='Название ВУЗа обязательно'),
        Length(min=2, max=100, message='Название ВУЗа должно быть от 2 до 100 символов')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "ВлГУ им. А.Г. и Н.Г. Столетовых"
    })

    # Пароль
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен содержать минимум 6 символов'),
        EqualTo('confirm_password', message='Пароли должны совпадать')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "Введите пароль"
    })

    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Подтверждение пароля обязательно')
    ], render_kw={
        # "class": "form-control",
        "placeholder": "Повторите пароль"
    })

    submit = SubmitField('Зарегистрироваться', render_kw={
        "class": "btn btn-primary w-100"
    })

    # Кастомные валидаторы
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован. Используйте другой.')


class LoginForm(FlaskForm):
    # Данные для входа
    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=3, max=120, message='Должно быть от 3 до 120 символов')
    ], render_kw={
        "placeholder": "Введите имя пользователя",
        "autocomplete": "username"
    })

    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=1, message='Введите пароль')
    ], render_kw={
        "placeholder": "Введите ваш пароль",
        "autocomplete": "current-password"
    })

    remember_me = BooleanField('Запомнить меня')

    next = HiddenField()

    submit = SubmitField('Войти', render_kw={
        "class": "btn btn-primary w-100"
    })


class CreateNoteForm(FlaskForm):
    title = StringField('Название конспекта', validators=[
        DataRequired(message='Название обязательно'),
        Length(min=2, max=250, message='Название должно быть от 2 до 250 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Введите название конспекта"
    })

    subject = StringField('Предмет', validators=[
        DataRequired(message='Название предмета обязательно'),
        Length(min=2, max=100, message='Название предмета должно быть от 2 до 100 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Например: Базы данных и экспертные системы"
    })

    teacher = StringField('Преподаватель', validators=[
        Length(max=100, message='ФИО преподавателя не должно превышать 100 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Иванов Иван Иванович"
    })

    # Скрытое поле для контента из Quill редактора
    content = TextAreaField('Контент', validators=[
        DataRequired(message='Контент не может быть пустым')
    ], render_kw={
        "class": "d-none"  # Скрываем, так как будет Quill
    })

    submit = SubmitField('Создать конспект', render_kw={
        "class": "btn btn-primary btn-lg w-100"
    })


# Аналогично форме создания
class UpdateNoteForm(FlaskForm):
    title = StringField('Название конспекта', validators=[
        DataRequired(message='Название обязательно'),
        Length(min=2, max=250, message='Название должно быть от 2 до 250 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Введите название конспекта"
    })

    subject = StringField('Предмет', validators=[
        DataRequired(message='Название предмета обязательно'),
        Length(min=2, max=100, message='Название предмета должно быть от 2 до 100 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Например: Базы данных и экспертные системы"
    })

    teacher = StringField('Преподаватель', validators=[
        Length(max=100, message='ФИО преподавателя не должно превышать 100 символов')
    ], render_kw={
        "class": "form-control",
        "placeholder": "Иванов Иван Иванович"
    })

    # Скрытое поле для контента из Quill редактора
    content = TextAreaField('Контент', validators=[
        DataRequired(message='Контент не может быть пустым')
    ], render_kw={
        "class": "d-none"  # Скрываем, так как будет Quill
    })

    submit = SubmitField('Обновить конспект', render_kw={
        "class": "btn btn-primary btn-lg w-100"
    })