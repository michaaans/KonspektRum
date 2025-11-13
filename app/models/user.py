import random

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(200))
    full_name = db.Column(db.String(100)) # ФИО
    university = db.Column(db.String(100)) # ВУЗ
    avatar = db.Column(db.String(50), default='avatar_1.png') # аватарка
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_teacher(self):
        return self.role.name == "teacher"

    @property
    def is_admin(self):
        return self.role.name == "admin"

    @staticmethod
    def get_random_avatar():
        avatar_number = random.randint(1, 6)
        return f'avatar_{avatar_number}.png'
