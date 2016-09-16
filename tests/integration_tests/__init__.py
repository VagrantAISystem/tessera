import pytest

def setup_function(module):
    """Clears out the database and re seeds it for the tests."""
    if os.path.isfile(tessera.app.config.DEFAULT_DB_LOCATION):
        os.remove(tessera.app.config.DEFAULT_DB_LOCATION)
    import seeds

def teardown_function(module):
    """Removes the database after the tests."""
    if os.path.isfile(tessera.app.config.DEFAULT_DB_LOCATION):
        os.remove(tessera.app.config.DEFAULT_DB_LOCATION)
