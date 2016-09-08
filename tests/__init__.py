import tessera
import os
import json
import pytest

from jsonschema import validate

def setup_module(module):
    """Clears out the database and re seeds it for the tests."""
    if os.path.isfile(tessera.app.config.TEST_DB_LOCATION):
        os.remove(tessera.app.config.TEST_DB_LOCATION)
    import seeds

def teardown_module(module):
    """Removes the database after the tests."""
    if os.path.isfile(tessera.app.config.TEST_DB_LOCATION):
        os.remove(tessera.app.config.TEST_DB_LOCATION)

def get_token(admin):
    if admin:
        return tessera.lib.tokens.create_token(1)
    return tessera.lib.tokens.create_token(2)

def test_json(jsn, schema):
    try:
        validate(jsn, schema)
        return True
    except Exception as e:
        print(e)
        return False

def t_post(route, payload):
    """Tests a post request with no auth"""
    with tessera.app.test_client() as client:
        response = client.post(route, data=json.dumps(payload),
                               content_type="application/json")
    return response

def t_get(route):
    """Tests a get request with no auth"""
    with tessera.app.test_client() as client:
        response = client.get(route)
    return response

def t_put(route, payload):
    """Tests a put request with no auth"""
    with tessera.app.test_client() as client:
        response = client.put(route, data=json.dumps(payload),
                              content_type="application/json")
    return response

def t_delete(route):
    """Tests a delete request with no auth"""
    with tessera.app.test_client() as client:
        response = client.delete(route)
    return response

def a_post(route, payload, admin=False):
    """Tests a post request with auth"""
    token = get_token(admin) 
    with tessera.app.test_client() as client:
        response = client.post(route, data=json.dumps(payload),
                               content_type="application/json",
                               headers={ "Authorization": token })
    return response

def a_get(route, admin=False):
    """Tests a get request with auth"""
    token = get_token(admin)    
    with tessera.app.test_client() as client:
        response = client.get(route, headers={ "Authorization": token })
    return response

def a_put(route, payload, admin=False):
    """Tests a put request with auth"""
    token = get_token(admin)    
    with tessera.app.test_client() as client:
        response = client.put(route, data=json.dumps(payload),
                              content_type="application/json",
                              headers={ "Authorization": token })
    return response

def a_delete(route, admin=False):
    """Tests a delete request with auth"""
    token = get_token(admin)    
    with tessera.app.test_client() as client:
        response = client.delete(route, headers={ "Authorization": token })
    return response


