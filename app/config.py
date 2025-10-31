import os


class Config(object):
    USER = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'konspektrumflask')
    HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    PORT = os.environ.get('POSTGRES_PORT', 5432)
    DATABASE = os.environ.get('POSTGRES_DATABASE', 'flask_konspekt_db')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    SECRET_KEY = 'a92925e67d659c7552691e6f70b2013dc963b73a20b9be99b04bad3edccb7b4e'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

