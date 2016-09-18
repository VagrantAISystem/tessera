import tests

class TestRoleRoutes():
    # Create
    def test_member_create():
        r = tests.t_post("/api/v1/roles/the-a-team/TEST2",
                         {
                             "user": {
                                 "username": "test",
                             },
                             "role": "admin",
                         })
        assert r.status_code == 401
        r = tests.t_post("/api/v1/roles/the-a-team/TEST2",
                         {
                             "user": {
                                 "username": "test",
                             },
                             "role": "admin",
                         })
        assert r.status_code == 200

    # Read
    def test_member_get():
        r = tests.a_get("/api/v1/roles/the-a-team/0")
        assert r.status_code == 200

    # Update
    def test_member_update():
        r = tests.t_put("/api/v1/roles/the-a-team/0",
                        {
                            "name": "Not Administrator",
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/roles/the-a-team/0",
                        {
                            "name": "Not Administrator",
                        })
        assert r.status_code == 200

    # Delete
    def test_member_delete():
        r = tests.t_delete("/api/v1/roles/the-a-team/0")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/roles/the-a-team/0")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/roles/the-a-team/0")
        assert r.status_code == 404
