from tessera import app
from tessera.v1.models import Team, Project
from tessera.lib import AppError
from flask import jsonify, g
from tessera.v1 import v1


@v1.route("/projects", methods=["GET"])
def project_all():
    return jsonify( [ p.to_json() for p in Project.query.all() ] )

@v1.route("/projects/<int:i>", methods=["GET"])
def project_get_id(i):
    p = Project.query.filter(Project.id == i).first()
    if p == None:
        raise AppError(status_code=404,
                       message="Project not found.")
    return jsonify( p.to_json() )

@v1.route("/<string:team>/projects", methods=["GET"])
def project_index(team):
    t = Team.query.filter_by(url_stub=team).first()
    return jsonify([ p.to_json() for p in t.projects.all() ])

@v1.route("/<string:team>/<string:pkey>", methods=["GET"])
def project_get(team, pkey):
    t = Team.get_by_name_or_stub(team)
    p = t.projects.filter_by(pkey=pkey).first()
    if p == None:
        raise AppError(status_code=404,
                       message="That project does not exist.")
    return jsonify( p.to_json() )

@v1.route("/<string:team>/<string:pkey>/members", methods=["GET"])
def project_members_index(team, pkey):
    t = Team.query.filter_by(url_stub=team).first()

