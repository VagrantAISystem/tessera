import tests

class TestProjectRoutes():
    # Create
    def test_project_create():
        r = tests.t_post("/api/v1/projects",
                         {
                             "name": "The C Project",
                             "description": "A unit testing experience.",
                             "project_lead": {
                                 "username": "testadmin",
                             },
                         })
        assert r.status_code == 401
        r = tests.a_post("/api/v1/projects",
                         {
                             "name": "The C Project",
                             "description": "A unit testing experience.",
                             "project_lead": {
                                 "username": "testadmin",
                             },
                         })
        assert r.status_code == 200

    # Read
    def test_project_get():
        r = tests.a_get("/api/v1/projects/the-a-team/TEST")
        assert r.status_code == 200

    # Update
    def test_project_update():
        r = tests.a_put("/api/v1/projects/the-a-team/TEST",
                        {
                            "name": "The A Project",
                            "description": "A unit testing experience.",
                            "project_lead": {
                                "username": "testadmin",
                            },
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/projects/the-a-team/TEST",
                        {
                            "name": "The A Project",
                            "description": "A unit testing experience.",
                            "project_lead": {
                                "username": "testadmin",
                            },
                        })
        assert r.status_code == 200

        # Delete
    def test_project_delete():
        r = tests.t_delete("/api/v1/projects/the-a-team/TEST2")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/projects/the-a-team/TEST2")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/projects/the-a-team/TEST2")
        assert r.status_code == 404
