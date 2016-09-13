from tessera import db
from tessera.models.v1.base import Base
from sqlalchemy.orm import joinedload
from tessera.models.v1.team import Team


class Project(Base):
    """Project is a container for tickets."""
    pkey     = db.Column(db.String(6), nullable=False, unique=True)
    name     = db.Column(db.String(250), nullable=False)
    repo     = db.Column(db.String(250))
    homepage = db.Column(db.String(250))

    project_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))

    tickets = db.relationship('Ticket', backref='project')
    members = db.relationship('Membership', backref='project', lazy='dynamic')

    def __init__(self, *, pkey, name, repo='', homepage=''):
        self.pkey     = pkey.upper()
        self.name     = name
        self.repo     = repo
        self.homepage = homepage

    def get_by_key(team_slug, pkey, preload=False):
        p = Project.query.\
                options(joinedload(Project.project_lead)).\
                join(Project.team).\
                filter(Team.url_slug == team_slug).\
                filter(Project.pkey == pkey).\
                first()
        if p == None:
            raise AppError(status_code=404, message="Project not found.")
        return p

    def to_json(self):
        return super().to_json(ignoreFields=["updated_at"])

    def __repr__(self):
        return "<Project %r>" % (self.pkey)
