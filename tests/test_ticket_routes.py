import tests
import json
from tessera.models.v1.schemas import ticket_test_schema

# Create
def test_ticket_create():
    r = tests.t_post("/api/v1/the-a-team/TEST/tickets",
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
    assert tests.test_json(jsn, ticket_test_schema)

# Read
def test_ticket_get():
    r = tests.a_get("/api/v1/the-a-team/TEST/TEST-1")
    jsn = json.loads(r.data.decode("utf-8"))
    assert tests.test_json(jsn, ticket_test_schema)

# Update
def test_ticket_update():
    r = tests.t_put("/api/v1/the-a-team/TEST/TEST-1", 
                    {
                        "summary": "This is not a unit test ticket.",
                        "description": "I hope this unit test passes.",
                        "reporter": {
                            "username": "testadmin",
                        },
                    })
    assert r.status_code == 401
    r = tests.a_put("/api/v1/the-a-team/TEST/TEST-1", 
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
def test_ticket_delete():
    r = tests.a_delete("/api/v1/the-a-team/TEST/TEST-2")
    assert r.status_code == 401
    r = tests.a_delete("/api/v1/the-a-team/TEST/TEST-2")
    assert r.status_code == 200
    r = tests.a_get("/api/v1/the-a-team/TEST/TEST-1")
    assert r.status_code == 404
