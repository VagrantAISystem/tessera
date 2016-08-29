from sqlite3 import IntegrityError
from tessera import cache, db, app
from tessera.lib.models import User
from tessera.lib.tokens import create_token, auth_required, admin_required
from flask import jsonify, request, g
from tessera.api import API

@API.route("/users", methods=["GET"])
@auth_required
@admin_required
def user_index():
    users = [ u.serialize() for u in User.query.all() ]
    print(users)
    return jsonify(users)

@API.route("/users", methods=["POST"])
def user_create():
    ujson = request.get_json()
    u = User(username=ujson.get("username", ""),
             password=ujson.get("password", ""),
             full_name=ujson.get("full_name", ""),
             email=ujson.get("email", "")) 
    db.session.add(u)
    try:
        db.session.commit()
        ujson = u.serialize()
        ujson["token"] = create_token(u.id)
        return jsonify(ujson)
    except IntegrityError as ie:
        app.logger.error(str(ie))
        r = jsonify(message="That username is already taken.")
        r.status_code = 409
        return r
    except Exception as e:
        r = jsonify(message="Unexpected error.")
        app.logger.error(str(e))
        r.status_code = 500
        return r
