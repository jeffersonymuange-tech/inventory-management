# Tests for the menu actions that change data.
# cli_api.requests.request is faked, so no server is needed.
import requests
from unittest.mock import patch

import cli_change
from helpers import ITEM, make_response


@patch("cli_api.requests.request")
def test_add_item(mock_request, capsys):
    mock_request.return_value = make_response(201, ITEM)
    cli_change.add_item("Oat Milk", 3.5, 10)
    assert "Item added" in capsys.readouterr().out
    sent = mock_request.call_args.kwargs["json"]
    assert sent["product_name"] == "Oat Milk"
    assert sent["price"] == 3.5


@patch("cli_api.requests.request")
def test_update_item(mock_request, capsys):
    mock_request.return_value = make_response(200, ITEM)
    cli_change.update_item(1, price=4.25)
    assert mock_request.call_args.kwargs["json"] == {"price": 4.25}
    assert "Item updated" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_update_item_nothing_given(mock_request, capsys):
    cli_change.update_item(1)
    assert "nothing to update" in capsys.readouterr().out
    mock_request.assert_not_called()


@patch("cli_api.requests.request")
def test_delete_item(mock_request, capsys):
    mock_request.return_value = make_response(200, {"message": "Item deleted"})
    cli_change.delete_item(1)
    assert "Item deleted" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_import_item(mock_request, capsys):
    mock_request.return_value = make_response(201, ITEM)
    cli_change.import_item("123", 2.5, 4)
    assert mock_request.call_args.kwargs["json"] == {"barcode": "123", "price": 2.5, "quantity": 4}
    assert "Imported" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_api_error_is_shown(mock_request, capsys):
    mock_request.return_value = make_response(502, {"error": "Could not connect to OpenFoodFacts"})
    cli_change.import_item("123", 1, 1)
    assert "OpenFoodFacts" in capsys.readouterr().out


@patch("cli_api.requests.request", side_effect=requests.ConnectionError())
def test_server_not_running(mock_request, capsys):
    cli_change.delete_item(1)
    assert "Could not connect" in capsys.readouterr().out
