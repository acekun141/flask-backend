import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
            'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
