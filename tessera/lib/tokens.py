import config
import jwt

from datetime import timedelta
from datetime import datetime as dt

from tessera import app

from functools import wraps
from flask import g, request, jsonify


def create_token(sub):
    payload = {
        'sub': sub,
        'iat': dt.utcnow(),
        'exp': dt.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    token = req.headers.get('Authorization')
    return jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing Authorizaiton Header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except jwt.DecodeError as e:
            response = jsonify(message='Token is invalid.')
            response.status_code = 401
            app.logger.error(e)
            return response
        except jwt.ExpiredSignature as e:
            response = jsonify(message='Token has expired.')
            response.status_code = 401
            app.logger.info(e)
            return response

        g.user_id = payload['sub']
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    """admin_required will make sure the user has admin privilegeds before
    executing the decorated function. It MUST follow an auth_required decorator
    or else it will fail."""
    @wraps(f)
    @auth_required
    def decorated_function(*args, **kwargs):
        # Are you logged in?
        if g.user_id == None:
            response = jsonify(message='You are not logged in.')
            response.status_code = 401
            return response

        # Are you an admin?
        u = User.filter(User.id == g.user_id).first()
        if not u.is_admin:
            response = jsonify(message='You are not an Administrator.')
            response.status_code = 403
            return response

        # Else user is an admin and logged in so just execute.
        return f(*args, **kwargs)

    return decorated_function

