"""Utilities that are used throughout Tessera

This module contains various convenviences that are used throughout the entire
application
"""

from functools import wraps
from flask import session
from flask.json import jsonify

class AppError(Exception):
    def __init__(self, *, status_code, message):
        self.message = message
        self.code = status_code
