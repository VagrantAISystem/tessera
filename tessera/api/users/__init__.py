from tessera.lib.models import User
from flask import jsonify
from tessera.api import API

@API.route("/users", methods=["GET"])
def index():
    users = [ u.serialize() for u in User.query.all() ]
    print(users)
    return jsonify(users)
