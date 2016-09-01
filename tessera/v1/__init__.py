from flask import Blueprint

v1 = Blueprint("v1", __name__, url_prefix='/api/v1')

import tessera.v1.users
import tessera.v1.tokens
import tessera.v1.teams
import tessera.v1.projects
