import tessera
import pytest

import seeds

@pytest.fixture
def client():
    return tessera.app.test_client()


