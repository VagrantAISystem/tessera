from tessera import db
from tessera.v1.models.base import Base

class Project(Base):
    """Project is a container for tickets."""
    pkey     = db.Column(db.String(6), nullable=False, unique=True)
    name     = db.Column(db.String(250), nullable=False)
    repo     = db.Column(db.String(250))
    homepage = db.Column(db.String(250))

    project_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))

    tickets = db.relationship('Ticket', backref='project', lazy='dynamic')
    members = db.relationship('Membership', backref='project', lazy='dynamic')

    def __init__(self, *, pkey, name, repo='', homepage=''):
        self.pkey     = pkey.upper()
        self.name     = name
        self.repo     = repo
        self.homepage = homepage

    def __repr__(self):
        return "<Project %r>" % (self.pkey)


