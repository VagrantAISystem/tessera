from jsonschema import validate
from tessera.models.v1.schemas import ticket_test_schema
from tessera.models.v1 import Ticket
from tessera import db

class TestTicketModel():
    def test_get_ticket_by_id(self):
        tk = Ticket.get_by_id(0)
        assert tk != None

    def test_get_ticket_by_key(self):
        tk = Ticket.get_by_key("the-a-team", "TEST", "TEST-1")
        assert tk != None

    def test_ticket_to_json(self):
        tk = Ticket.query.first()
        assert validate(tk.to_json(), ticket_test_schema) == None

    def test_ticket_from_json(self):
        tk = Ticket.from_json("TEST", {
            "summary": "Integration Test From JSON",
            "description": "I hope this passes",
            "reporter": { "username": "test" },
            "assignee": { "username": "test" },
        })
        db.session.add(tk)
        db.session.commit()
        db.session.rollback()
