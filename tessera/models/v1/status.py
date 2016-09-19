import enum

from tessera import db
from sqlalchemy import CheckConstraint
from tessera.models.v1 import Base

class Status(Base):
    __tablename__ = "statuses"

    name          = db.Column(db.String(100), nullable=False)
    status_type   = db.Column(db.Enum("TODO", "IN_PROGRESS", "DONE", name='status_types'))
    next_statuses = db.relationship('Status',
                                    secondary=status_relationships,
                                    primaryjoin="Status.id == status_relationships.c.status_id",
                                    secondaryjoin="Status.id == status_relationships.c.next_status_id",
                                    backref='previous_statuses',
                                    lazy='dynamic')

    tickets = db.relationship('Ticket', backref='status', lazy='dynamic')

    def __init__(self, *, name, status_type=0):
        self.name        = name
        self.status_type = status_type

    def to_json(self):
        return super().to_json(ignoreFields=["created_at", "updated_at"])

    def get_next(self):
        return self.next_statuses.all()

    def get_previous(self):
        return self.previous_statuses.all()
