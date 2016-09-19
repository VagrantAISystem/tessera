import enum

from tessera import db
from tessera.lib import AppError
from tessera.models.v1.base import Base

class DataTypes(enum.Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    TEXT = "TEXT"

project_field_schema = db.Table(
    'project_field_schema',
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'),
              nullable=False),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'),
              nullable=False),
    db.PrimaryKeyConstraint('field_id', 'project_id')
)

class Field(Base):
    name      = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.Enum("INTEGER", "FLOAT", "STRING", "TEXT",
                                  name="data_types"), nullable=False)

class FieldValue(Base):
    field_id      = db.Column('field_id', db.Integer,
                              db.ForeignKey('field.id'), nullable=False)
    ticket_id     = db.Column('ticket_id', db.Integer,
                              db.ForeignKey('ticket.id'), nullable=False)
    text_value    = db.Column(db.Text())
    string_value  = db.Column(db.String(250))
    float_value   = db.Column(db.Float)
    integer_value = db.Column(db.Integer)

    def validate_value(self):
        if (
            (self.field.data_type == DataTypes.INTEGER and type(self.value) is not int) or
            (self.field.data_type == DataTypes.FLOAT and type(self.value) is not float) or
            (self.field.data_type == DataTypes.TEXT and type(self.value) is not str) or
            (self.field.data_type == DataTypes.STRING and type(self.value) is not str)
           ):
            raise AppError(status_code=400, message='Invalid type for the field: ' + self.name)

    def set_value(self):
        self.validate_value()
        if self.field.data_type == DataTypes.INTEGER:
            self.integer_value = self.value
        elif self.field.data_type == DataTypes.FLOAT:
            self.float_value  = self.value
        elif self.field.data_type == DataTypes.TEXT:
            self.text_value =  self.value
        elif self.field.data_type == DataTypes.STRING:
            self.string_value = self.value
        else:
            raise AppError(status_code=500,
                           message='Uknown error setting field value')

    def from_json(jsn):
        parent_field = Field.query.filter_by(name=jsn.get("name", ""))
        if parent_field == None:
            raise AppError(status_code=404, message="No field with that name")
        fv = FieldValue(name=jsn.get("name"),
                        value=jsn.get("value"))
        fv.set_value()
        return fv
