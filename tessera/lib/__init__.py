"""Utilities that are used throughout Tessera

This module contains various convenviences that are used throughout the entire
application
"""

import re
from functools import wraps

under_pat = under_pat = re.compile(r'_([a-z])')

def to_camel_case(snake_str):
    return under_pat.sub(lambda x: x.group(1).upper(), snake_str)

class AppError(Exception):
    def __init__(self, *, status_code, message):
        self.message = message
        self.code = status_code
