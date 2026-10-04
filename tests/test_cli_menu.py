# Tests for typing in numbers and for the menu itself.
# The keyboard (input) and the API are both faked.
from unittest.mock import patch

import cli
from cli_input import ask_whole_number, ask_price
from helpers import ITEM, make_response


@patch("builtins.input", side_effect=["abc", "5"])
def test_ask_whole_number_retries(mock_input, capsys):
    assert ask_whole_number("Number: ") == 5
    assert "whole number" in capsys.readouterr().out


@patch("builtins.input", side_effect=["x", "4.99"])
def test_ask_price_retries(mock_input):
    assert ask_price("Price: ") == 4.99


@patch("builtins.input", side_effect=["9", "0"])
def test_menu_bad_option_then_quit(mock_input, capsys):
    cli.main()
    out = capsys.readouterr().out
    assert "not a valid option" in out
    assert "Bye!" in out


@patch("cli_api.requests.request")
@patch("builtins.input", side_effect=["1", "0"])
def test_menu_view_all(mock_input, mock_request, capsys):
    mock_request.return_value = make_response(200, [ITEM])
    cli.main()
    assert "Organic Almond Milk" in capsys.readouterr().out
