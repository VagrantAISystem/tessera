import enum

from tessera import db
from tessera.v1.models.base import Base

class DataTypes(enum.Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    TEXT = "TEXT"

custom_field_ticket_value = db.Table(
    'custom_field_value',
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'),
              nullable=False),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'),
              nullable=False),
    db.Column('text_value', db.Text()),
    db.Column('string_value', db.String(250)),
    db.Column('float_value', db.Float),
    db.Column('integer_value', db.Integer),
    db.PrimaryKeyConstraint('status_id', 'next_status_id')
) 

class FieldSchema(Base):
    field_id = db.Column('field_id', db.Integer, db.ForeignKey('field.id'))

class Field(Base):
    name      = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.Enum(DataTypes), nullable=False)
    value     = db.relationship()
