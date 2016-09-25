import enum

from tessera import db
from sqlalchemy import CheckConstraint
from tessera.models.v1 import Base

class Status(Base):
    __tablename__ = "statuses"

    name          = db.Column(db.String(100), nullable=False)
    status_type   = db.Column(db.Enum("TODO", "IN_PROGRESS", "DONE", name='status_types'),
                              nullable=False)
    def to_json(self):
        return super().to_json(ignoreFields=["created_at", "updated_at"])
