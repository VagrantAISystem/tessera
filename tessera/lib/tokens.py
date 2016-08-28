import config
import jwt
import datetime as dt

from functools import wraps
from flask import g


def create_token(sub):
    payload = {
        'sub': sub,
        'iat': dt.utcnow(),
        'exp': dt.utcnow() + dt.timedelta(days=1)
    }

    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
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
        except jwt.DecodeError:
            response = jsonify(message='Token is invalid.')
            response.status_code = 401
            return response
        except jwt.ExpiredSignature:
            response = jsonify(message='Token has expired.')
            response.status_code = 401
            return response

        g.user_id = payload['sub']
        return f(*args, **kwargs)

    return decorated_function
