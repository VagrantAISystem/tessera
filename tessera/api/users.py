from tessera.lib.models import User
from tessera.lib.tokens import auth_required
from flask import jsonify
from tessera.api import API

@API.route("/users", methods=["GET"])
@auth_required
def index():
    users = [ u.serialize() for u in User.query.all() ]
    print(users)
    return jsonify(users)
