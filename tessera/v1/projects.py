from tessera import app
from tessera.v1.models import Team
from tessera.lib import AppError
from flask import jsonify, g
from tessera.v1 import v1

@v1.route("/projects", methods=["GET"])
def project_index_all():
    return jsonify([ p.to_json() for p in Project.query.all() ])

@v1.route("/<string:team_slug>/projects", methods=["GET"])
def project_index(team_slug):
    t = Team.query.\
            join(Team.projects).\
            filter(Team.url_slug == team_slug).\
            first()
    if t == None:
        raise AppError(status_code=404, message="Team not found.")
    return jsonify([ p.to_json() for p in t.projects ])

@v1.route("/<string:team_slug>/<string:pkey>", methods=["GET"])
def project_get(team_slug, pkey):
    p = Project.query.\
            join(Project.team).\
            filter(Team.url_slug == team_slug).\
            filter(Project.pkey == pkey).\
            first()
    if p == None:
        raise AppError(status_code=404,
                       message="That project does not exist.")
    return jsonify( p.to_json() )

@v1.route("/<string:team_slug>/<string:pkey>/members", methods=["GET"])
def project_members_index(team_slug, pkey):
    m = Membership.query.\
            join(Membership.project).\
            join(Membership.user).\
            join(Project.team).\
            filter(Team.url_slug == url_slug).\
            filter(Project.pkey == pkey).\
            all()
    if m == None:
        raise AppError(status_code=404, message="Project or team not found.")
    return m
