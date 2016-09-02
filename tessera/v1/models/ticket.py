from tessera import db
from tessera.v1.models.project import Project
from tessera.v1.models.team import Team
from tessera.v1.models.base import Base
from sqlalchemy.orm import joinedload

class Ticket(Base):
    """A ticket is a unit of work for a project, be it a bug or support ticket."""
    ticket_key  = db.Column(db.String(100), nullable=False, unique=True) # I mean jesus christ how many digits
    summary     = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text())

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'))
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, *, ticket_key, 
                          summary, 
                          description, 
                          assignee_id=None,
                          reporter_id=None):
        self.ticket_key  = ticket_key
        self.summary     = summary
        self.description = description
        self.assignee_id = assignee_id
        self.reporter_id = reporter_id

    def get_by_key(team_slug, pkey, ticket_key, preload=''):
        tk = Ticket.query.\
                options(joinedload(Ticket.reporter)).\
                options(joinedload(Ticket.assignee)).\
                join(Ticket.project).\
                join(Project.team).\
                filter(Team.url_slug == team_slug).\
                filter(Project.pkey == pkey).\
                filter(Ticket.ticket_key == ticket_key)

        if 'project' in preload.lower():
            tk = tk.options(joinedload(Ticket.project))

        tk = tk.first()
        if tk == None:
            raise AppError(status_code=404, message='Ticket not found.')
        return tk

    def to_json(self):
        s = super().to_json()
        s.pop('reporter_id', None)
        s.pop('assignee_id', None)
        s.pop('project_id', None)
        s.pop('status_id')
        s['ticketKey'] = s.pop('ticket_key')
        return s

    def __repr__(self):
        return '<Ticket %r>' % (self.ticket_key)


