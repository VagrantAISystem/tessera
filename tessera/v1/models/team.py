from tessera import db
from tessera.v1.models.base import Base

class Team(Base):
    """Team is a container for projects."""
    name     = db.Column(db.String(120), nullable=False, unique=True)
    url_stub = db.Column(db.String(150), nullable=False, unique=True)
    icon     = db.Column(db.String(150))    

    team_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    projects = db.relationship('Project', backref='team', lazy='dynamic')
    members  = db.relationship('Membership', backref='team', lazy='dynamic')
    
    def __init__(self, name, icon=""):
        self.name     = name
        self.url_stub = name.lower().replace(" ", "-")
        icon          = icon

    def set_name(self, name):
        self.name = name
        self.url_stub = name.lower().replace(" ", "-")

    def __repr__(self):
        return "<Team %r>" % (self.name)
