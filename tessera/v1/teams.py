from tessera import app
from tessera.v1.models import Team
from flask import jsonify, request, g
from tessera.v1 import v1

@v1.route("/teams", methods=["GET"])
def team_index():
    teams = [ t.to_json() for t in Team.query.all() ]
    return jsonify(teams)

@v1.route("/teams", methods=["POST"])
def team_create():
    tjson = request.get_json()
    t = Team.from_json(tjson)

@v1.route("/<string:team>", methods=["GET"])
def team_get_name(team):
    t = Team.get_by_name_or_stub(team)
    return jsonify( t.to_json() )

@v1.route("/teams/<int:i>", methods=["GET"])
def team_get_id(i):
    t = Team.query.filter_by(id=i).first()
    return jsonify( t.to_json() )

