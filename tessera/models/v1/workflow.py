from tessera import db
from tessera.v1.models.base import Base
from tessera.v1.models.relationships import workflow_transitions

class Workflow(Base):
    """Workflow is a container for ticket statuses."""
    __tablename__ = "workflows"

    name = db.Column(db.String(100), nullable=False)
    statuses = db.relationship('WorkflowStatuses', backref="workflow")

class WorkflowStatuses(db.Model):
    __tablename__ = "workflow_statuses"

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'),
                            primary_key=True)

    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'),
                            primary_key=True)

    next_statuses = db.relationship('Status',
                                    secondary=workflow_transitions,
                                    primaryjoin="Status.id == status_relationships.c.status_id",
                                    secondaryjoin="Status.id == status_relationships.c.next_status_id",
                                    backref='previous_statuses',
                                    lazy='dynamic')

    tickets = db.relationship('Ticket', backref='status', lazy='dynamic')

    def get_next(self):
        return self.next_statuses.all()

    def get_previous(self):
        return self.previous_statuses.all()
