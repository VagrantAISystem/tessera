"""Utilities that are used throughout Tessera

This module contains various convenviences that are used throughout the entire
application
"""

from functools import wraps
from flask import session
from flask.json import jsonify

def requires_login(f):
    """This decorator protects a route behind authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user_id'] is None:
            err = jsonify({ "error_message": "Not authorized." })
            err.status_code = 403
            return err
        return f(*args, **kwargs)
    return decorated_function
