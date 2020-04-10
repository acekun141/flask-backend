from flask import Blueprint

todo = Blueprint('todo', __name__, url_prefix='/todo')

from app.todo import models, routes
