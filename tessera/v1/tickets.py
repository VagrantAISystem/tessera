from flask import jsonify, request, g
from tessera.v1 import v1
from tessera.v1.models import Ticket, Project, Team

@v1.route("/tickets", methods=["GET"])
def ticket_index_all():
    return jsonify([ t.to_json() for t in Ticket.query.all() ])

@v1.route("/<string:team_slug>/<string:pkey>/tickets", methods=["GET"])
def ticket_index(team_slug, pkey):
    p = Project.\
            query.\
            join(Project.team).\
            join(Project.tickets).\
            filter(Project.pkey == pkey).\
            filter(Team.url_slug == team_slug).\
            first()
    return jsonify([ tk.to_json() for tk in p.tickets ])

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>", methods=["GET"])
def ticket_get(team_slug, pkey, ticket_key):
    tk = Ticket.query.\
            join(Ticket.project).\
            join(Project.team).\
            filter(Team.url_slug == team_slug).\
            filter(Project.pkey == pkey).\
            filter(Ticket.ticket_key == ticket_key).\
            first()
    if tk == None:
        raise AppError(status_code=404, message="Ticket not found.")
    return jsonify( tk.to_json() )
