from tessera import db
from sqlalchemy.orm import joinedload
from tessera.models.v1.base import Base
from tessera.models.v1.team import Team
from tessera.models.v1.schemas import project_schema


class Project(Base):
    """Project is a container for tickets."""
    pkey     = db.Column(db.String(6), nullable=False, unique=True)
    name     = db.Column(db.String(250), nullable=False)
    repo     = db.Column(db.String(250))
    homepage = db.Column(db.String(250))

    project_lead_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))

    tickets = db.relationship('Ticket', backref='project')
    members = db.relationship('Membership', backref='project', lazy='dynamic')

    def __init__(self, *, pkey, name, repo='', homepage=''):
        self.pkey     = pkey.upper()
        self.name     = name
        self.repo     = repo
        self.homepage = homepage

    def get_by_id(i, preload=''):
       p = Project.query.\
                options(joinedload(Project.project_lead)).\
                filter(Project.id == i).\
                first()
       return p

    def get_by_key(team_slug, pkey, preload=''):
        p = Project.query.\
                options(joinedload(Project.project_lead)).\
                join(Project.team).\
                filter(Team.url_slug == team_slug).\
                filter(Project.pkey == pkey).\
                first()
        return p

    def from_json(team_slug, jsn):
        validate(jsn, project_schema)
        t = Team.get_by_slug(team_slug)
        p = Project(pkey=jsn["pkey"],
                    name=jsn["name"],
                    homepage=jsn.get("homepage", ""),
                    repo=jsn.get("repo", ""))
        p.team = t
        return p

    def to_json(self):
        return super().to_json(ignoreFields=["updated_at"])

    def __repr__(self):
        return "<Project %r>" % (self.pkey)
