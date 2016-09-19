import tests

class TestStatusRoutes():
    # Create
    def test_status_create():
        r = tests.t_post("/api/v1/statuses",
                         {
                             "name": "Integration Testing",
                             "status_type": "DONE",
                         })
        assert r.status_code == 401
        r = tests.a_post("/api/v1/statuses",
                         {
                             "name": "Integration Testing",
                             "status_type": "DONE",
                         })
        assert r.status_code == 200

    # Read
    def test_status_get():
        r = tests.t_get("/api/v1/statuses/0")
        assert r.status_code == 401
        r = tests.a_get("/api/v1/statuses/0")
        assert r.status_code == 200

    # Update
    def test_status_update():
        r = tests.t_put("/api/v1/statuses/1",
                        {
                            "name": "Integration Test 2"
                        })
        assert r.status_code == 401
        r = tests.a_put("/api/v1/statuses/1",
                        {
                            "name": "Integration Test 2"
                        })
        assert r.status_code == 200

    # Delete
    def test_status_delete():
        r = tests.t_delete("/api/v1/statuses/2")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/statuses/2")
        assert r.status_code == 403
        r = tests.a_delete("/api/v1/statuses/2", admin=True)
        assert r.status_code == 200
