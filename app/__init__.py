from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.todo import todo as todo_blueprint
    app.register_blueprint(todo_blueprint)
    return app
