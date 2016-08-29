from tessera import db
from tessera.v1.models.base import Base

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
        permission_level = perm

    def __repr__(self):
        return "<Membership %r %r %r %r>"  % (self.team_id, self.project_id,
                                              self.user_id,
                                              self.permission_level)
