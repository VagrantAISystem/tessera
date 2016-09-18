import os
import config

def setup_module():
    """Creates a test database and re seeds it for the tests. Will clean up after itself"""
    if os.path.isfile(config.DEFAULT_DB_LOCATION):
        os.remove(config.DEFAULT_DB_LOCATION)
    import seeds
