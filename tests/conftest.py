# This file is read by pytest automatically.
import pytest

from app import app
from database import reset_inventory


@pytest.fixture
def client():
    # Runs before every test so each test starts with fresh data
    reset_inventory()
    app.config["TESTING"] = True
    return app.test_client()
