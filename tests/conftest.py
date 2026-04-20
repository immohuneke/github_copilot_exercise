import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities database before each test."""
    original_state = copy.deepcopy(activities_store)
    yield
    activities_store.clear()
    activities_store.update(copy.deepcopy(original_state))


@pytest.fixture
def client():
    return TestClient(app)
