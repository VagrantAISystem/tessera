from jsonschema import validate
from tessera.models.v1.schemas import team_schema
from tessera.models.v1 import Team
from tessera import db

class TestTeamModel():
    def test_get_team_by_id(self):
        t = Team.get_by_id(0)
        assert t != None

    def test_get_team_by_key(self):
        t = Team.get_by_slug("the-a-team")
        assert t != None

    def test_team_to_json(self):
        t = Team.query.first()
        assert validate(t.to_json(), team_schema) == None

    def test_team_from_json(self):
        t = Team.from_json({
            "name": "The Integration Test Team",
            "teamLead": { "username": "testadmin" },
            "description": "Integration Test Team",
        })
        db.session.add(t)
        db.session.commit()
        db.session.rollback()
