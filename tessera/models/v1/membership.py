from tessera import db
from tessera.models.v1.base import Base

class Membership(Base):
    """Membership is used to control access and permissions for a project or
    team.
    
    Permission levels are stored as Integers and there are three permission
    levels.

    0 = User
    1 = Contributor
    2 = Administrator
    """
    team_id     = db.Column(db.Integer, db.ForeignKey('team.id'))
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))

    permission_level = db.Column(db.Integer)

    def __init__(self, perm):
        self.permission_level = perm

    def get_project_memberships(team_slug, pkey):
        m = Membership.query.\
                join(Membership.project).\
                join(Membership.user).\
                join(Project.team).\
                filter(Team.url_slug == url_slug).\
                filter(Project.pkey == pkey).\
                all()
        if m == None:
            raise AppError(status_code=404, message="Project or team not found.")
        return m

    def __repr__(self):
        return "<Membership %r %r %r %r>"  % (self.team_id, self.project_id,
                                              self.user_id,
                                              self.permission_level)
