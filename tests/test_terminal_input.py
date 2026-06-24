import pytest
from input.action import Action
from input.terminal import TerminalInput


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


def test_action_none(monkeypatch, terminal_input):
    monkeypatch.setattr("builtins.input", lambda _: "h")
    monkeypatch.setattr("builtins.input", lambda _: "gg")
    monkeypatch.setattr("builtins.input", lambda _: "12")
    assert terminal_input.get_action() == Action.NONE
