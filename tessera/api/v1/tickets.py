from flask import jsonify, request, g
from tessera.api.v1 import v1
from tessera import db
from tessera.models.v1 import Ticket, Project, Comment

@v1.route("/tickets", methods=["GET"])
def ticket_index_all():
    return jsonify([ t.to_json() for t in Ticket.query.all() ])

@v1.route("/<string:team_slug>/<string:pkey>/tickets", methods=["GET"])
def ticket_index(team_slug, pkey):
    p = Project.get_tickets(team_slug, pkey)
    return jsonify([ tk.to_json() for tk in p.tickets ])

@v1.route("/<string:team_slug>/<string:pkey>/tickets", methods=["POST"])
def ticket_create(team_slug, pkey):
    jsn = request.get_json()
    p = Project.get_by_key(team_slug, pkey)
    tk = Ticket.from_json(p, jsn)
    db.session.add(tk)
    db.session.commit()
    return jsonify(tk.to_json())

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

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>/comments", methods=["GET"])
def comment_index(team_slug, pkey, ticket_key):
    cmts = Comment.get_all(team_slug, pkey, ticket_key)
    return jsonify([ c.to_json() for c in cmts ])

@v1.route("/<string:team_slug>/<string:pkey>/<string:ticket_key>/comments", methods=["POST"])
def comment_create(team_slug, pkey, ticket_key):
    j = request.get_json()
    c = Comment.from_json(j)
    tk = Ticket.get_by_key(team_slug, pkey, ticket_key)
    tk.comments.append(c)
    db.session.add(tk)
    db.session.commit()
    return jsonify(message="Comment successfully added.")
