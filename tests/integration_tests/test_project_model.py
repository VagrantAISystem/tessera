from jsonschema import validate
from tessera.models.v1.schemas import project_schema
from tessera.models.v1 import Project
from tessera import db

class TestProjectModel():
    def test_get_project_by_id(self):
        p = Project.get_by_id(0)
        assert p != None

    def test_get_project_by_key(self):
        p = Project.get_by_key("the-a-team", "TEST")
        assert p != None

    def test_project_to_json(self):
        p = Project.query.first()
        assert validate(p.to_json(), project_schema) == None

    def test_project_from_json(self):
        p = Project.from_json("the-b-team", {
            "pkey": "ITEST1",
            "name": "Integration Test Project",
            "repo": "https://github.com/chasinglogic/tessera",
        })
        db.session.add(p)
        db.session.commit()
        db.session.rollback()
