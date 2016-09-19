import tests

class TestTicketRoutes():
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
        assert r.status_code == 200

    # Read
    def test_ticket_get(self):
        r = tests.a_get("/api/v1/tickets/the-a-team/TEST/TEST-1")
        assert r.status_code == 200

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
        assert r.status_code == 200

    # Delete
    def test_ticket_delete(self):
        r = tests.t_delete("/api/v1/tickets/the-a-team/TEST/TEST-10")
        assert r.status_code == 401
        r = tests.a_delete("/api/v1/tickets/the-a-team/TEST/TEST-10")
        assert r.status_code == 200
        r = tests.a_get("/api/v1/tickets/the-a-team/TEST/TEST-10")
        assert r.status_code == 404
