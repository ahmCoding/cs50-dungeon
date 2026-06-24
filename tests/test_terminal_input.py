import pytest

from game.input.action import Action
from game.input.terminal import TerminalInput


@pytest.fixture
def terminal_input():
    return TerminalInput()


def test_action_up(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "w")
    assert terminal_input.get_action() == Action.MOVE_UP


def test_action_down(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "s")
    assert terminal_input.get_action() == Action.MOVE_DOWN


def test_action_left(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "a")
    assert terminal_input.get_action() == Action.MOVE_LEFT


def test_action_right(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "d")
    assert terminal_input.get_action() == Action.MOVE_RIGHT


def test_action_quit(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert terminal_input.get_action() == Action.QUIT


@pytest.mark.parametrize(
    "key,expected",
    [
        ("g", Action.NONE),
        ("w", Action.MOVE_UP),
        ("ss", Action.NONE),
    ],
)
def test_action_none(monkeypatch, terminal_input, key, expected):
    monkeypatch.setattr("builtins.input", lambda _: key)
    assert terminal_input.get_action() == expected
