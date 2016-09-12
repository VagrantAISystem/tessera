import config
import jwt

from datetime import timedelta
from datetime import datetime as dt

from tessera import app, cache
from tessera.models.v1 import User

from tessera.lib import AppError

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
            raise AppError(message="Missing Authorizaiton Header", 
                           status_code = 401)
        try:
            payload = parse_token(request)
        except jwt.DecodeError as e:
            raise AppError(message="Token is invalid", status_code = 401)
        except jwt.ExpiredSignature as e:
            raise AppError(message="Token has expired.", status_code = 401)
        g.user = User.get_by_username_or_id(payload['sub'])
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
            raise AppError(message="You are not logged in.", 
                           status_code = 401)
        # Are you an admin?
        u = User.filter(User.id == g.user_id).first()
        if not u.is_admin:
            raise AppError(message='You are not an Administrator.',
                           status_code = 403)

        # Else user is an admin and logged in so just execute.
        return f(*args, **kwargs)

    return decorated_function

