import tessera.lib.tokens as tk

from tessera.lib.models import User
from flask import jsonify, g, request
from tessera.api import API
from tessera import cache, app

@API.route("/sessions", methods=["POST"])
def create():
    ujson = request.get_json()

    u = User.query.filter_by(username=ujson.get("username", "")).first()
        
    if u == None:
        r = jsonify(message="Invalid username.")
        r.status_code = 404
        return r

    if u.check_password(ujson.get("password", "")):
        tkn = tk.create_token(u.id)
        cache.set(u.id, u.serialize())
        return jsonify(token=tkn)

    r = jsonify(message="Invalid password.")
    r.status_code = 401
    return r
 
@API.route("/sessions/<user_id>", methods=["DELETE"])
@tk.auth_required
def destroy(user_id):
    if g.user_id == int(user_id):
        cache.delete(user_id)
        return jsonify(message="Session successfully removed.")
    r = jsonify(message="You do not have permission to remove that session.")
    r.status_code = 403
    return r
