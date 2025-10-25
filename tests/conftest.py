import pytest
from fastapi.testclient import TestClient

from fastapi_model.app import app


@pytest.fixture
def client():
    return TestClient(app)
