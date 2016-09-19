from tessera import db
from tessera.lib import AppError
from tessera.models.v1.project import Project
from tessera.models.v1.team import Team
from tessera.models.v1.user import User
from tessera.models.v1.base import Base
from tessera.models.v1.schemas import ticket_schema
from sqlalchemy.orm import joinedload
from jsonschema import validate

class TicketType(Base):
    __tablename__ = "ticket_types"

    name = db.Column(db.String(250), nullable=False, unique=True)

class Ticket(Base):
    """A ticket is a unit of work for a project, be it a bug or support ticket."""
    __tablename__ = "tickets"

    ticket_key  = db.Column(db.String(100), nullable=False, unique=True)
    summary     = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text())

    assignee_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    reporter_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id     = db.Column(db.Integer, db.ForeignKey('projects.id'))
    status_id      = db.Column(db.Integer, db.ForeignKey('status.id'))
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('issue_types.id'))

    fields      = db.relationship('FieldValue', backref='ticket')
    comments    = db.relationship('Comment', backref='ticket', lazy='dynamic')

    def get_by_id(i, preload=''):
        tk = Ticket.query.\
                options(joinedload(Ticket.status)).\
                options(joinedload(Ticket.reporter)).\
                options(joinedload(Ticket.assignee)).\
                filter(Ticket.id == i)
        return tk.first()

    def get_by_key(team_slug, pkey, ticket_key, preload=''):
        tk = Ticket.query.\
                options(joinedload(Ticket.status)).\
                options(joinedload(Ticket.reporter)).\
                options(joinedload(Ticket.assignee)).\
                join(Ticket.project).\
                join(Project.team).\
                filter(Team.url_slug == team_slug).\
                filter(Project.pkey == pkey).\
                filter(Ticket.ticket_key == ticket_key)
        if 'project' in preload.lower():
            tk = tk.options(joinedload(Ticket.project))
        return tk.first()

    def from_json(pkey, json):
        validate(json, ticket_schema)
        prjct = Project.get_by_key(pkey)
        r = User.get_by_username_or_id(json.get("reporter", {}).get("username", ""))
        a = User.get_by_username_or_id(json.get("assignee", {}).get("username", ""))
        tk = Ticket(summary=json['summary'],
                    description=json['description'])
        tk.assignee_id = a.id
        tk.reporter_id = r.id
        tk.project_id  = prjct.id
        return tk

    def from_json(prjct, json):
        validate(json, ticket_schema)
        r = User.get_by_username_or_id(json.get("reporter", {}).get("username", ""))
        a = User.get_by_username_or_id(json.get("assignee", {}).get("username", ""))
        t = Ticket(summary=json['summary'],
                   description=json['description'],
                   ticket_key=prjct.pkey + "-" + str(len(prjct.tickets) + 1),
                   reporter_id=r.id,
                   project_id=prjct.id)
        if a != None:
            tk.assignee_id = a.id
        return tk

    def __repr__(self):
        return '<Ticket %r>' % (self.ticket_key)
