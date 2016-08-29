from tessera import db
from tessera.v1.models import Base

class Ticket(Base):
    """A ticket is a unit of work for a project, be it a bug or support ticket."""
    ticket_key  = db.Column(db.String(100), nullable=False, unique=True) # I mean jesus christ how many digits
    summary     = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text())

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, ticket_key, summary, description):
        self.ticket_key  = ticket_key
        self.summary     = summary
        self.description = description

    def __repr__(self):
        return "<Ticket %r>" % (self.ticket_key)


