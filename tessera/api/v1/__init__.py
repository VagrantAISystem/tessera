from flask import Blueprint

v1 = Blueprint("v1", __name__, url_prefix='/api/v1')

import tessera.api.v1.users
import tessera.api.v1.tokens
import tessera.api.v1.teams
import tessera.api.v1.projects
import tessera.api.v1.tickets
