# Tests for the menu actions that only look at data.
# cli_api.requests.request is faked, so no server is needed.
from unittest.mock import patch

import cli_view
from helpers import ITEM, make_response


@patch("cli_api.requests.request")
def test_view_all(mock_request, capsys):
    mock_request.return_value = make_response(200, [ITEM])
    cli_view.view_all()
    assert "Organic Almond Milk" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_view_all_empty(mock_request, capsys):
    mock_request.return_value = make_response(200, [])
    cli_view.view_all()
    assert "empty" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_view_one(mock_request, capsys):
    mock_request.return_value = make_response(200, ITEM)
    cli_view.view_one(1)
    assert "Silk" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_view_one_not_found(mock_request, capsys):
    mock_request.return_value = make_response(404, {"error": "Item not found"})
    cli_view.view_one(99)
    assert "Item not found" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_find_by_barcode(mock_request, capsys):
    mock_request.return_value = make_response(200, ITEM)
    cli_view.find_by_barcode("123")
    assert "Organic Almond Milk" in capsys.readouterr().out


@patch("cli_api.requests.request")
def test_find_by_name(mock_request, capsys):
    mock_request.return_value = make_response(200, [ITEM, ITEM])
    cli_view.find_by_name("almond")
    assert capsys.readouterr().out.count("Organic Almond Milk") == 2


@patch("cli_api.requests.request")
def test_find_by_name_no_results(mock_request, capsys):
    mock_request.return_value = make_response(200, [])
    cli_view.find_by_name("zzz")
    assert "No products found" in capsys.readouterr().out
