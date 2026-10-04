# Tests for POST /inventory/import (OpenFoodFacts is faked with patch)
from unittest.mock import patch

from helpers import FAKE_PRODUCT
from off_api import OpenFoodFactsError


@patch("external_routes.get_product_by_barcode", return_value=FAKE_PRODUCT)
def test_import_item(mock_get, client):
    response = client.post("/inventory/import", json={"barcode": "111", "price": 2.5, "quantity": 9})
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Test Spread"
    assert len(client.get("/inventory").get_json()) == 4


@patch("external_routes.get_product_by_barcode", return_value=None)
def test_import_item_not_found(mock_get, client):
    response = client.post("/inventory/import", json={"barcode": "000"})
    assert response.status_code == 404


@patch("external_routes.get_product_by_barcode", side_effect=OpenFoodFactsError("down"))
def test_import_item_api_down(mock_get, client):
    response = client.post("/inventory/import", json={"barcode": "111"})
    assert response.status_code == 502


def test_import_item_duplicate(client):
    response = client.post("/inventory/import", json={"barcode": "3017620422003"})
    assert response.status_code == 409


def test_import_item_needs_barcode(client):
    response = client.post("/inventory/import", json={})
    assert response.status_code == 400
