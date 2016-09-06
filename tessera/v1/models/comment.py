from tessera import db
from tessera.v1.models.base import Base
from tessera.v1.models.team import Team
from tessera.v1.models.project import Project
from tessera.v1.models.ticket import Ticket
from tessera.v1.models.user import User
from sqlalchemy.orm import joinedload

class Comment(Base):
    """A comment on a ticket"""
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))

    body      = db.Column(db.Text())

    def __init__(self, ticket=None, author=None, *, body):
        self.ticket = ticket
        self.author = author
        self.body   = body

    def to_json(self):
        s = super().to_json()
        s.pop('author_id', None)
        s.pop('ticket_id', None)
        return s

    def from_json(json):
        validate(json, comment_schema)
        u = User.get_by_username_or_id(j['author']['username'])
        c = Comment(body=json['body'], author=u)
        return c

    def get_all(team_slug, pkey, ticket_key):
        cmts = Comment.query.\
                options(joinedload(Comment.author)).\
                join(Comment.ticket).\
                join(Ticket.project).\
                join(Project.team).\
                filter(Ticket.ticket_key == ticket_key).\
                filter(Project.pkey == pkey).\
                filter(Team.url_slug == team_slug).\
                all()
        return cmts

    def get_for_ticket(ticket):
        cmts = Comment.query.\
                join(Comment.ticket).\
                filter(Comment.ticket_id == ticket.id)
        return cmts

comment_schema = {
    'type': 'object',
    'properties': {  
        'body': { 'type': 'string' },
        'author': { 
            'type': 'object',
            'properties': {
                'username': { 'type': 'string' },
                'email': { 'type': 'string' },
                'fullName': { 'type': 'string' },
            },
            'required': [ 'username' ],
        },
    },
    'required': [ 'body', 'author' ],
}
