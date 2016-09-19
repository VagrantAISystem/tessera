from tessera import db
from tessera.models.v1.base import Base
from sqlalchemy.orm import joinedload
from tessera.models.v1.team import Team

project_ticket_type_workflows = db.Table(
    "project_ticket_type_workflows",
    db.Column("workflow_id", db.ForeignKey("workflows.id"), nullable=False),
    db.Column("project_id", db.ForeignKey("projects.id"), nullable=False),
    db.Column("ticket_type_id", db.ForeignKey("ticket_types.id")),
    db.PrimaryKeyConstraint("workflow_id", "project_id")
)

class Project(Base):
    """Project is a container for tickets."""
    __tablename__ = "projects"

    pkey     = db.Column(db.String(6), nullable=False, unique=True)
    name     = db.Column(db.String(250), nullable=False)
    repo     = db.Column(db.String(250))
    homepage = db.Column(db.String(250))

    project_lead_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team_id         = db.Column(db.Integer, db.ForeignKey('teams.id'))

    tickets = db.relationship('Ticket', backref='project')
    members = db.relationship('Membership', backref='project', lazy='dynamic')

    workflows = db.relationship('Workflow',
                                secondary=project_ticket_type_workflows,
                                primaryjoin="Project.id == project_ticket_type_workflows.project_id",
                                secondaryjoin="Workflow.id == project_ticket_type_workflows.workflow_id",
                                backref='project',
                                lazy="dynamic")

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
