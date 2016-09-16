import pytest
import os
import config

@pytest.fixture(scope="module")
def db(request):
    """Clears out the database and re seeds it for the tests.
    then removes the database after the tests."""
    if os.path.isfile(config.DEFAULT_DB_LOCATION):
        os.remove(config.DEFAULT_DB_LOCATION)
    import seeds
    yield None
    if os.path.isfile(config.DEFAULT_DB_LOCATION):
        os.remove(config.DEFAULT_DB_LOCATION)
