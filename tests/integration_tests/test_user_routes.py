import tests

class TestUserRoutes():
    # Create
    def test_user_create():
        r = tests.t_post("/api/v1/users",
                         {
                             "username": "integrationtest",
                             "email": "test200@example.com",
                             "fullName": "Integration Test",
                         })
        assert r.status_code == 200

    # Read
    def test_user_get():
        r = tests.t_get("/api/v1/users/chasinglogic")
        assert r.status_code == 200

    # Update
    def test_user_update():
        r = tests.t_put("/api/v1/users/chasinglogic",
                        {
                            "fullName": "Not Mathew Robinson",
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/users/chasinglogic",
                        {
                            "fullName": "Not Mathew Robinson",
                        })
        assert r.status_code == 403
        r = tests.a_put("/api/v1/users/chasinglogic",
                        {
                            "fullName": "Not Mathew Robinson",
                        },
                        admin=True)
        assert r.status_code == 200

    # Delete
    def test_user_delete():
        r = tests.t_delete("/api/v1/users/lionize")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/users/lionize")
        assert r.status_code == 403
        r = tests.a_delete("/api/v1/users/lionize", admin=True)
        assert r.status_code == 200
        r = tests.a_get("/api/v1/users/lionize")
        assert r.status_code == 404
