from app.auth import auth as blueprint
from flask import request, jsonify, current_app
from flask.views import MethodView
from app.auth.models import User, UserInfo
from functools import wraps
import jwt


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if ('x-access-token' in request.headers):
            token = request.headers['x-access-token']
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'])
                user = User.query.filter_by(public_id=payload['public_id']).first()
                if not user:
                    raise Exception('Cannot Authorization')
                return f(current_user=user, *args, **kwargs)
            except:
                return jsonify({'error': 'Cannot Authorization'}), 401
        else:
            return jsonify({'error': 'Cannot Authorization'}), 401

    return wrapped


def create_token(user):
    '''Return token with user

    Parameters
    ----------
    user : User object

    Returns
    -------
    token : str
        Token of user for authorization
    '''
    payload = {}
    payload['public_id'] = user.public_id
    payload['username'] = user.username
    user_info = UserInfo.query.filter_by(user_id=user.id).first()
    if user_info:
        payload['first_name'] = user_info.first_name
        payload['last_name'] = user_info.last_name
    token = jwt.encode(payload, current_app.config['SECRET_KEY'])
    return token


class UserAPI(MethodView):

    def get(self):
        auth = request.authorization
        if not auth:
            return jsonify({'error': 'Cannot Authorization'}), 401
        username = auth.get('username')
        password = auth.get('password')
        if (username and password):
            user = User.query.filter_by(username=username).first()
            if (user and user.check_password(password)):
                token = create_token(user)
                return jsonify({'token': token.decode('utf-8')})
        return jsonify({'error': 'Cannot Authorization'}), 401

    def post(self):
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        if (username and password and
                first_name and last_name):
            new_user = User.create(username, password)
            if new_user:
                UserInfo.create(new_user.id, first_name, last_name)
                return jsonify({'message': 'Successful'})
            else:
                return jsonify({'error': 'Username has been registered'}), 404
        return jsonify({'error': 'Cannot perform'}), 404

blueprint.add_url_rule(rule='/', view_func=UserAPI.as_view('user_api'))


class UserDetailAPI(MethodView):

    def get(self):
        pass

    def post(self):
        pass


blueprint.add_url_rule(rule='/<int:user_id>',
                       view_func=UserDetailAPI.as_view('user_detail_api'))
