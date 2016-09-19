from tessera import db
from tessera.v1.models.base import Base

# This table shows us our workflow, we query our next statuses by getting all
# rows with a given status_id and then we can find our previous statuses by
# getting all the rows with next_status_id = our id.
status_relationships = db.Table(
    'workflow_status_relationships',
    db.Column('workflow_status_id', db.Integer,
              db.ForeignKey('workflow_statuses.id'), nullable=False),
    db.Column('status_id', db.Integer,
              db.ForeignKey('workflow_statuses.status_id'), nullable=False),
    db.Column('next_status_id', db.Integer, db.ForeignKey('status.id'),
              nullable=False),
    db.PrimaryKeyConstraint('workflow_status_id', 'status_id', 'next_status_id')
)

class Workflow(Base):
    """Workflow is a container for ticket statuses."""
    __tablename__ = "workflows"

    name = db.Column(db.String(100), nullable=False)
    statuses = db.relationship('WorkflowStatuses',
                               backref="workflow")

class WorkflowStatuses(db.Model):
    __tablename__ = "workflow_statuses"

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'),
                            primary_key=True)
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'),
                            primary_key=True)
    next_statuses = db.relationship('Status',
                                    secondary=status_relationships,
                                    primaryjoin="Status.id == status_relationships.c.status_id",
                                    secondaryjoin="Status.id == status_relationships.c.next_status_id",
                                    backref='previous_statuses',
                                    lazy='dynamic')
    tickets = db.relationship('Ticket', backref='status', lazy='dynamic')

    def get_next(self):
        return self.next_statuses.all()

    def get_previous(self):
        return self.previous_statuses.all()
