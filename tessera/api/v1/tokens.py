import tessera.lib.tokens as tk

from tessera.v1.models import User
from flask import jsonify, g, request
from tessera.v1 import v1
from tessera import cache, app

@v1.route("/tokens", methods=["POST"])
def session_create():
    ujson = request.get_json()
    u = User.query.filter_by(username=ujson.get("username", "")).first()
        
    if u == None:
        raise AppError(message="Invalid username/password.",
                       status_code = 401)

    if u.check_password(ujson.get("password", "")):
        tkn = tk.create_token(u.id)
        return jsonify(token=tkn)

    raise AppError(message="Invalid username/password.", status_code = 401)
 
@v1.route("/tokens/<int:user_id>", methods=["DELETE"])
@tk.auth_required
def session_destroy(user_id):
    if g.user.id == user_id:
        cache.delete(user_id)
        return jsonify(message="Session successfully removed.")

    raise AppError(message="You do not have permission to remove that session.",
                   status_code = 403)
