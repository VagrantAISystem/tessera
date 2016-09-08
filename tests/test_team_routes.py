import tests
import json
from tessera.v1.models.schemas import team_schema

# Create
def test_team_create():
    r = tests.t_post("/api/v1/teams",
                     {
                         "name": "The B Team",
                         "description": "A unit testing experience.",
                         "project_lead": {
                             "username": "testadmin",
                         },
                     })
    assert r.status_code == 401
    r = tests.a_post("/api/v1/teams",
                     {
                         "name": "The B Team",
                         "description": "A unit testing experience.",
                         "project_lead": {
                             "username": "testadmin",
                         },
                     })
    jsn = json.loads(r.data.decode("utf-8"))
    assert tests.test_json(jsn, team_schema)

# Read
def test_team_get():
    r = tests.a_get("/api/v1/the-a-team")
    jsn = json.loads(r.data.decode("utf-8"))
    assert tests.test_json(jsn, team_schema)

# Update
def test_team_update():
    r = tests.a_put("/api/v1/teams",
                     {
                         "name": "The A Team",
                         "description": "A unit testing experience.",
                         "project_lead": {
                             "username": "testadmin",
                         },
                     })
    assert r.status_code == 401
    r = tests.a_put("/api/v1/teams",
                     {
                         "name": "The A Team",
                         "description": "A unit testing experience.",
                         "project_lead": {
                             "username": "testadmin",
                         },
                     })
    jsn = json.loads(r.data.decode("utf-8"))
    assert tests.test_json(jsn, team_schema)
    assert jsn == {
        "name": "The A Team",
        "description": "A unit testing experience.",
        "icon": None,
        "project_lead": {
            "username": "testadmin",
            "fullName": "Test Testerson",
            "email": "test@example.com",
        },
    }

# Delete
def test_team_delete():
    r = tests.t_delete("/api/v1/the-a-team")
    assert r.status_code == 401
    r = tests.a_delete("/api/v1/the-a-team")
    assert r.status_code == 200
    r = tests.a_get("/api/v1/the-a-team")
    assert r.status_code == 404
