import enum

from tessera import db
from sqlalchemy import CheckConstraint
from tessera.models.v1 import Base

# This table shows us our workflow, we query our next statuses by getting all
# rows with a given status_id and then we can find our previous statuses by
# getting all the rows with next_status_id = our id.
status_relationships = db.Table(
    'status_relationships',
    db.Column('status_id', db.Integer, db.ForeignKey('status.id'),
              nullable=False),
    db.Column('next_status_id', db.Integer, db.ForeignKey('status.id'),
              nullable=False),
    db.PrimaryKeyConstraint('status_id', 'next_status_id')
)

class StatusType(enum.Enum):
    TODO        = "To Do"
    IN_PROGRESS = "In Progress"
    DONE        = "Done"


class Status(Base):
    name          = db.Column(db.String(100), nullable=False)
    status_type   = db.Column(db.Enum(StatusType))
    next_statuses = db.relationship('Status', 
                                    secondary=status_relationships,
                                    primaryjoin="Status.id == status_relationships.c.status_id",
                                    secondaryjoin="Status.id == status_relationships.c.next_status_id", 
                                    backref='previous_statuses',
                                    lazy='dynamic')

    tickets = db.relationship('Ticket', backref='status', lazy='dynamic')

    __table_args__ = (
        CheckConstraint(status_type<3, name='check_type_less_than_three'),
        CheckConstraint(status_type>=0, name='check_type_positive'),
        {})

    def __init__(self, *, name, status_type=0):
        self.name        = name
        self.status_type = status_type

    def to_json(self):
        s = super().to_json()
        s.pop("createdDate", None)
        s.pop("updatedDate", None)
        s["statusType"] = s.pop("status_type")
        return s

    def get_next(self):
        return self.next_statuses.all()
    
    def get_previous(self):
        return self.previous_statuses.all()

