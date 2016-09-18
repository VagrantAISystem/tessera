from jsonschema import validate
from tessera.models.v1.schemas import role_schema
from tessera.models.v1 import Role
from tessera import db

class TestRoleModel():
    def test_get_role_by_id(self):
        r = Role.get_by_id(0)
        assert r != None

    def test_get_role_by_key(self):
        r = Role.get_by_name("ADMINISTRATOR")
        assert r != None

    def test_role_to_json(self):
        r = Role.query.first()
        assert validate(r.to_json(), role_schema) == None
