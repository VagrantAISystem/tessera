import tests
import json
from tessera.v1.models.schemas import ticket_test_schema

# Create
def test_ticket_create():
    r = tests.a_post("/api/v1/the-a-team/TEST/tickets",
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
    assert jsn == { "message": "Ticket successfully created." }

# Read
def test_ticket_get():
    r = tests.a_get("/api/v1/the-a-team/TEST/TEST-1")
    jsn = json.loads(r.data.decode("utf-8"))
    assert tests.test_json(jsn, ticket_test_schema)

# Update
# Delete
