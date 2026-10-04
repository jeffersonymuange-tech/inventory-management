# Tests for the OpenFoodFacts search routes.
# The real website is never called, we fake it with patch.
from unittest.mock import patch

from helpers import FAKE_PRODUCT
from off_api import OpenFoodFactsError


@patch("external_routes.get_product_by_barcode", return_value=FAKE_PRODUCT)
def test_search_by_barcode(mock_get, client):
    response = client.get("/search/barcode/111")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Test Spread"


@patch("external_routes.get_product_by_barcode", return_value=None)
def test_search_by_barcode_not_found(mock_get, client):
    response = client.get("/search/barcode/000")
    assert response.status_code == 404


@patch("external_routes.get_product_by_barcode", side_effect=OpenFoodFactsError("down"))
def test_search_by_barcode_api_down(mock_get, client):
    response = client.get("/search/barcode/111")
    assert response.status_code == 502


@patch("external_routes.search_products", return_value=[FAKE_PRODUCT])
def test_search_by_name(mock_search, client):
    response = client.get("/search?name=spread")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_search_by_name_needs_a_name(client):
    response = client.get("/search")
    assert response.status_code == 400
