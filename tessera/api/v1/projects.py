from tessera import app
from tessera.lib.tokens import auth_required
from tessera.models.v1 import Team, Project
from tessera.lib import AppError
from flask import jsonify, g, request
from tessera.api.v1 import v1

@v1.route("/projects", methods=["GET"])
def project_index_all():
    return jsonify([ p.to_json() for p in Project.query.all() ])

# TODO: Should the query here be pulled into the Team model?
@v1.route("/teams/<string:team_slug>/projects", methods=["GET"])
def project_index(team_slug):
    t = Team.query.\
            join(Team.projects).\
            filter(Team.url_slug == team_slug).\
            first()
    if t == None:
        raise AppError(status_code=404, message="Team not found.")
    return jsonify([ p.to_json() for p in t.projects ])

@v1.route("/teams/<string:team_slug>/projects", methods=["POST"])
def project_create(team_slug):
    return jsonify(message="not implemented")

@v1.route("/teams/<string:team_slug>/<string:pkey>", methods=["GET"])
def project_get(team_slug, pkey):
    p = Project.get_by_key(team_slug, pkey, request.args.get("preload", False))
    return jsonify( p.to_json() )

@v1.route("/teams/<string:team_slug>/<string:pkey>", methods=["PUT"])
@auth_required
def project_update(team_slug, pkey):
    p = Project.get_by_key(team_slug, pkey)
    if g.user.id == p.project_lead_id or g.user.is_admin:
        p.update(request.get_json())
        db.session.add(p)
        db.session.commit()
        return jsonify(message="Project successfully updated.")
    raise AppError(status_code=403,
                   message="You are not permitted to perform that action")

@v1.route("/teams/<string:team_slug>/<string:pkey>/members", methods=["GET"])
def project_members_index(team_slug, pkey):
    m = Membership.get_project_memberships(team_slug, pkey)
    return m
