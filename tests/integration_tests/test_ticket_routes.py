import tests
import json
import pytest
from tessera.models.v1.schemas import ticket_test_schema

@pytest.mark.usefixtures("db")
class TestTicketRoutes:
    # Create
    def test_ticket_create(self):
        r = tests.t_post("/api/v1/tickets/the-a-team/TEST/tickets",
                         {
                             "summary": "This is a unit test ticket.",
                             "description": "I hope this unit test passes.",
                             "reporter": {
                                 "username": "test",
                                 "email": "test1@example.com",
                                 "fullName": "Test Testerson",
                             },
                         })
        assert r.status_code == 401
        r = tests.a_post("/api/v1/tickets/the-a-team/TEST/tickets",
                         {
                             "summary": "This is a unit test ticket.",
                             "description": "I hope this unit test passes.",
                             "reporter": {
                                 "username": "test",
                                 "email": "test1@example.com",
                                 "fullName": "Test Testerson",
                             },
                         })
        jsn = json.loads(r.data.decode("utf-8"))
        jsn["fields"] = [{"id": 0, "name": "test", "value": "TEST"}]
        assert tests.test_json(jsn, ticket_test_schema)

    # Read
    def test_ticket_get(self):
        r = tests.a_get("/api/v1/tickets/the-a-team/TEST/TEST-1")
        jsn = json.loads(r.data.decode("utf-8"))
        assert tests.test_json(jsn, ticket_test_schema)

    # Update
    def test_ticket_update(self):
        r = tests.t_put("/api/v1/tickets/the-a-team/TEST/TEST-1",
                        {
                            "summary": "This is not a unit test ticket.",
                            "description": "I hope this unit test passes.",
                            "reporter": {
                                "username": "testadmin",
                            },
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/tickets/the-a-team/TEST/TEST-1",
                        {
                            "summary": "This is not a unit test ticket.",
                            "description": "I hope this unit test passes.",
                            "reporter": {
                                "username": "testadmin",
                            },
                        })
        jsn = json.loads(r.data.decode("utf-8"))
        assert jsn == {
            "summary": "This is not a unit test ticket.",
            "description": "I hope this unit test passes.",
            "reporter": {
                "username": "testadmin",
            },
        }

    # Delete
    def test_ticket_delete(self):
        r = tests.t_delete("/api/v1/tickets/the-a-team/TEST/TEST-2")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/tickets/the-a-team/TEST/TEST-2")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/tickets/the-a-team/TEST/TEST-1")
        assert r.status_code == 404
