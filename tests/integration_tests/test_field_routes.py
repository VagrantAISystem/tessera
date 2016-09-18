import tests

class TestFieldRoutes():
    # Create
    def test_field_create(self):
        r = tests.t_post("/api/v1/fields",
                             {
                                 "name": "Unit Test Field",
                                 "data_type": "STRING",
                             })
        assert r.status_code == 401
        r = tests.a_post("/api/v1/fields",
                             {
                                 "name": "Unit Test Field",
                                 "data_type": "STRING",
                             })
        assert r.status_code == 200

    # Read
    def test_field_get(self):
        r = tests.t_get("/api/v1/fields/0")
        assert r.status_code == 404
        r = tests.a_get("/api/v1/fields/0")
        assert r.status_code == 200

    # Update
    def test_field_update(self):
        r = tests.t_put("/api/v1/fields/0",
                        {
                            "name": "Unit Test Update",
                        })
        assert r.status_code == 401
        r = tests.t_put("/api/v1/fields/0",
                        {
                            "name": "Unit Test Update",
                        })
        assert r.status_code == 200

    # Delete
    def test_field_delete(self):
        r = tests.t_delete("/api/v1/fields/1")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/fields/1")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/fields/1")
        assert r.status_code == 404
