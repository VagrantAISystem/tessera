from flask import jsonify, request, g
from tessera.v1 import v1
from tessera.v1.models import Ticket, Project, Team

@v1.route("/tickets", methods=["GET"])
def ticket_index_all():
    return jsonify([ t.to_json() for t in Ticket.query.all() ])

@v1.route("/<string:team_slug>/<string:pkey>/tickets", methods=["GET"])
def ticket_index(team_slug, pkey):
    p = Project.get_tickets(team_slug, pkey)
    return jsonify([ tk.to_json() for tk in p.tickets ])

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>", methods=["GET"])
def ticket_get(team_slug, pkey, ticket_key):
    prl = request.args.get("preload", "")
    tk = Ticket.get_by_key(team_slug, pkey, ticket_key, prl) 
    return jsonify( tk.to_json() )


@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>", methods=["PUT"])
def ticket_update(team_slug, pkey, ticket_key):
    return jsonify(message="Not implemented")

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>", methods=["DELETE"])
def ticket_delete(team_slug, pkey, ticket_key):
    return jsonify(message="Not implemented")

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>/next", methods=["GET"])
def ticket_next(team_slug, pkey, ticket_key):
    return jsonify(message="Not implemented")

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>/prev", methods=["GET"])
def ticket_prev(team_slug, pkey, ticket_key):
    return jsonify(message="Not implemented")
