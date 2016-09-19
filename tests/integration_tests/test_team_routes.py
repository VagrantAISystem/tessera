import tests

class TestTeamRoutes():
    # Create
    def test_team_create():
        r = tests.t_post("/api/v1/teams",
                         {
                             "name": "The C Team",
                             "description": "A unit testing experience.",
                             "project_lead": {
                                 "username": "testadmin",
                             },
                         })
        assert r.status_code == 401
        r = tests.a_post("/api/v1/teams",
                         {
                             "name": "The C Team",
                             "description": "A unit testing experience.",
                             "project_lead": {
                                 "username": "testadmin",
                             },
                         })
        assert r.status_code == 200

    # Read
    def test_team_get():
        r = tests.a_get("/api/v1/teams/the-a-team")
        assert r.status_code == 200

    # Update
    def test_team_update():
        r = tests.a_put("/api/v1/teams/the-a-team",
                        {
                            "name": "The A Team",
                            "description": "A unit testing experience.",
                            "project_lead": {
                                "username": "testadmin",
                            },
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/teams/the-a-team",
                        {
                            "name": "The A Team",
                            "description": "A unit testing experience.",
                            "project_lead": {
                                "username": "testadmin",
                            },
                        })
        assert r.status_code == 200

        # Delete
    def test_team_delete():
        r = tests.t_delete("/api/v1/teams/the-a-team")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/teams/the-a-team")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/teams/the-a-team")
        assert r.status_code == 404
