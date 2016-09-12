from tessera.models.v1 import Team
from flask import jsonify, request, g
from tessera.api.v1 import v1

@v1.route("/teams", methods=["GET"])
def team_index():
    teams = [ t.to_json() for t in Team.query.all() ]
    return jsonify(teams)

@v1.route("/teams", methods=["POST"])
def team_create():
    tjson = request.get_json()
    t = Team.from_json(tjson)

@v1.route("/<string:team_slug>", methods=["GET"])
def team_get(team_slug):
    t = Team.get_by_name_or_stub(team_slug)
    return jsonify( t.to_json() )

