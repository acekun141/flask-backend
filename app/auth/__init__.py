from flask import Blueprint

auth = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')

from app.auth import models, routes
