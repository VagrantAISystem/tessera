import enum

from tessera import db
from sqlalchemy import CheckConstraint
from tessera.models.v1 import Base

class Status(Base):
    __tablename__ = "statuses"

    name          = db.Column(db.String(100), nullable=False)
    status_type   = db.Column(db.Enum("TODO", "IN_PROGRESS", "DONE", name='status_types'))

    def to_json(self):
        return super().to_json(ignoreFields=["created_at", "updated_at"])

    def get_next(self):
        return self.next_statuses.all()

    def get_previous(self):
        return self.previous_statuses.all()
