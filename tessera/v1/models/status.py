from tessera import db
from tessera.v1.models import Base

class Status(Base):
    name        = db.Column(db.String(100), nullable=False)
    # workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'),
    #                         nullable=False) 
    next_status_id = db.Column(db.Integer, db.ForeignKey('status.id'),
                               nullable=False)
    prev_status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
