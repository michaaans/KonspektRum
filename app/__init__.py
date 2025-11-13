from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

from .routes.note import note
from .routes.main import main
from .routes.auth import auth
from .routes.profile import profile
from .routes.admin import admin


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(note)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(profile)
    app.register_blueprint(admin)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    with app.app_context():
        db.create_all()

    return app
