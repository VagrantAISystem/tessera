from tessera import db

# This table shows us our workflow, we query our next statuses by getting all
# rows with a given status_id and then we can find our previous statuses by
# getting all the rows with next_status_id = our id.
workflow_transitions = db.Table(
    'workflow_transitions',
    db.Column('workflow_status_id', db.Integer,
              db.ForeignKey('workflow_statuses.id'), nullable=False),
    db.Column('status_id', db.Integer,
              db.ForeignKey('workflow_statuses.status_id'), nullable=False),
    db.Column('next_status_id', db.Integer, db.ForeignKey('status.id'),
              nullable=False),
    db.PrimaryKeyConstraint('workflow_status_id', 'status_id', 'next_status_id')
)

# This assigns workflows to issue types per project
project_workflow_schemas = db.Table(
    "project_workflow_schemas",
    db.Column("workflow_id", db.ForeignKey("workflows.id"), nullable=False),
    db.Column("project_id", db.ForeignKey("projects.id"), nullable=False),
    db.Column("ticket_type_id", db.ForeignKey("ticket_types.id")),
    db.PrimaryKeyConstraint("workflow_id", "project_id")
)

