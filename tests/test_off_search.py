# Tests for search_products. requests.get is faked, no internet needed.
import pytest
from unittest.mock import patch

from helpers import GOOD_DATA, make_response
from off_api import search_products, OpenFoodFactsError


@patch("off_api.requests.get")
def test_search_finds_products(mock_get):
    mock_get.return_value = make_response(200, {"products": [GOOD_DATA["product"]]})
    results = search_products("almond milk")
    assert len(results) == 1
    assert results[0]["brands"] == "Silk"


@patch("off_api.requests.get")
def test_search_no_results(mock_get):
    mock_get.return_value = make_response(200, {"products": []})
    assert search_products("zzzz") == []


@patch("off_api.requests.get")
def test_search_server_error(mock_get):
    mock_get.return_value = make_response(503)
    with pytest.raises(OpenFoodFactsError):
        search_products("milk")
