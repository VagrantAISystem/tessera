from jsonschema import validate
from tessera.models.v1.schemas import user_schema
from tessera.models.v1 import User
from tessera import db

class TestUserModel():
    def test_get_user_by_id(self):
        u = User.get_by_username_or_id(0)
        assert u != None

    def test_get_user_by_username(self):
        u = User.get_by_username_or_id("chasinglogic")
        assert u != None

    def test_user_to_json(self):
        u = User.query.first()
        assert validate(u.to_json(), user_schema) == None

    def test_user_from_json(self):
        u = User.from_json({
            "username": "itest",
            "fullName": "Integration Test User",
            "email": "itest@example.com",
            "password": "test"
        })
        db.session.add(u)
        db.session.commit()
        db.session.rollback()
