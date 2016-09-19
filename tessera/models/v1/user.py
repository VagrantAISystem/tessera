from jsonschema import validate
from tessera import db
from tessera.models.v1 import Base
from tessera.models.v1.schemas import user_schema, user_signup_schema
from tessera.lib import AppError
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.exc import IntegrityError
from werkzeug import check_password_hash, generate_password_hash

class User(Base):
    """User represents a user of our application."""
    __tablename__ = "users"

    full_name = db.Column(db.String(250), nullable=False)
    email     = db.Column(db.String(128),  nullable=False, unique=True)
    # TODO: Move this into memberships
    is_admin  = db.Column(db.Boolean)
    username  = db.Column(db.String(128),  nullable=False, unique=True)
    password  = db.Column(db.String(192),  nullable=False)


    comments_author_of = db.relationship('Comment', backref='author',
                                         lazy='dynamic')
    projects_lead_of   = db.relationship('Project', backref='project_lead',
                                         lazy='dynamic')
    teams_lead_of      = db.relationship('Team', backref='team_lead',
                                         lazy='dynamic')
    memberships        = db.relationship('Membership', backref='user',
                                         lazy='dynamic')
    assigned_tickets   = db.relationship('Ticket', backref='assignee',
                                       lazy='dynamic',
                                       primaryjoin='Ticket.assignee_id == User.id')
    reported_tickets   = db.relationship('Ticket', backref='reporter',
                                       lazy='dynamic',
                                       primaryjoin='Ticket.reporter_id == User.id')

    teams    = association_proxy('membership', 'team')
    projects = association_proxy('membership', 'project')

    def get_by_username_or_id(param):
        try:
            i = int(param)
            u = User.query.filter(User.id == i).first()
        except:
            u = User.query.filter_by(username=param).first()
        if u == None:
            raise AppError(status_code=404, message='User not found.')
        return u

    def from_json(json):
        validate(json, user_signup_schema)
        u = User(username=json['username'],
                 password=json['password'],
                 full_name=json['fullName'],
                 email=json['email'])
        return u

    def to_json(self):
        """Extends base class to_json to drop password as well."""
        return super().to_json(ignoreFields=["password", "is_admin", "created_at", "updated_at"])

    def update(self, json):
        validate(self, user_schema)
        self.username = json.get('username', self.username)
        self.full_name = json.get('fullName', self.full_name)
        self.email = json.get('email', self.email)

        if json.get('password', None) != None:
            self.set_password(json['password'])

    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def __repr__(self):
        return '<User %r>' % (self.username)
