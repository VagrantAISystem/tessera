from tessera import db
from tessera.lib.models import Base
from werkzeug import check_password_hash, generate_password_hash

class User(Base):
    """User represents a user of our application."""

    full_name = db.Column(db.String(250), nullable=False)
    email     = db.Column(db.String(128),  nullable=False, unique=True)

    username  = db.Column(db.String(128),  nullable=False, unique=True)
    password  = db.Column(db.String(192),  nullable=False)

    def __init__(self, username, email, password, full_name):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(pw):
        self.password = generate_password_hash(pw)

    def check_password(pw):
        return check_password_hash(self.password, pw)

    def __repr__(self):
        return "<User %r>" % (self.name)

