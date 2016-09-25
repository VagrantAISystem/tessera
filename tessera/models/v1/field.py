import enum

from tessera import db
from tessera.lib import AppError
from tessera.models.v1.base import Base
from tessera.models.v1.relationships import project_field_schema

class DataTypes(enum.Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    TEXT = "TEXT"

class Field(Base):
    __tablename__ = "fields"

    name      = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.Enum("INTEGER", "FLOAT", "STRING", "TEXT",
                                  name="data_types"), nullable=False)

class FieldValue(Base):
    __tablename__ = "field_values"

    field_id      = db.Column('field_id', db.Integer,
                              db.ForeignKey('field.id'), nullable=False)
    ticket_id     = db.Column('ticket_id', db.Integer,
                              db.ForeignKey('ticket.id'), nullable=False)

    text_value    = db.Column('text_value', db.Text())
    string_value  = db.Column('string_value', db.String(250))
    float_value   = db.Column('float_value', db.Float)
    integer_value = db.Column('integer_value', db.Integer)

    def validate_value(self):
        if (
            (self.field.data_type == DataTypes.INTEGER and type(self.value) is not int) or
            (self.field.data_type == DataTypes.FLOAT and type(self.value) is not float) or
            (self.field.data_type == DataTypes.TEXT and type(self.value) is not str) or
            (self.field.data_type == DataTypes.STRING and type(self.value) is not str) or
            (self.value == None)
           ):
            return False
        return True

    def set_value(self):
        if self.field.data_type == DataTypes.INTEGER:
            self.integer_value = self.value
        elif self.field.data_type == DataTypes.FLOAT:
            self.float_value  = self.value
        elif self.field.data_type == DataTypes.TEXT:
            self.text_value =  self.value
        elif self.field.data_type == DataTypes.STRING:
            self.string_value = self.value
        else:
            self.value = None
        return self.validate_value()

    def from_json(jsn):
        parent_field = Field.query.filter_by(name=jsn.get("name", ""))
        if parent_field == None:
            raise AppError(status_code=404, message="No field with that name")
        fv = FieldValue(name=jsn.get("name"),
                        value=jsn.get("value"))
        fv.set_value()
        return fv
