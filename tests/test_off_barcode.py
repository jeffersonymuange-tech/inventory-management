# Tests for get_product_by_barcode. requests.get is faked, no internet needed.
import pytest
import requests
from unittest.mock import Mock, patch

from helpers import GOOD_DATA, make_response
from off_api import get_product_by_barcode, OpenFoodFactsError


@patch("off_api.requests.get")
def test_barcode_found(mock_get):
    mock_get.return_value = make_response(200, GOOD_DATA)
    product = get_product_by_barcode("123")
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"
    assert product["barcode"] == "123"


@patch("off_api.requests.get")
def test_barcode_status_zero(mock_get):
    mock_get.return_value = make_response(200, {"status": 0})
    assert get_product_by_barcode("000") is None


@patch("off_api.requests.get")
def test_barcode_404(mock_get):
    mock_get.return_value = make_response(404, {})
    assert get_product_by_barcode("000") is None


@patch("off_api.requests.get")
def test_barcode_server_error(mock_get):
    mock_get.return_value = make_response(500)
    with pytest.raises(OpenFoodFactsError):
        get_product_by_barcode("123")


@patch("off_api.requests.get", side_effect=requests.Timeout())
def test_barcode_no_connection(mock_get):
    with pytest.raises(OpenFoodFactsError):
        get_product_by_barcode("123")


@patch("off_api.requests.get")
def test_barcode_bad_json(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError()
    mock_get.return_value = response
    with pytest.raises(OpenFoodFactsError):
        get_product_by_barcode("123")


@patch("off_api.requests.get")
def test_missing_fields_get_defaults(mock_get):
    mock_get.return_value = make_response(200, {"status": 1, "product": {"code": "9"}})
    product = get_product_by_barcode("9")
    assert product["product_name"] == "Unknown product"
    assert product["brands"] == ""
