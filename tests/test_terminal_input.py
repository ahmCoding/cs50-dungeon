import pytest

from game.input.action import Action
from game.input.cbreak_terminal import CbreakTerminal


@pytest.fixture
def terminal_input():
    return CbreakTerminal()


@pytest.mark.parametrize(
    "key,expected_action",
    [
        ("w", Action.MOVE_UP),
        ("s", Action.MOVE_DOWN),
        ("d", Action.MOVE_RIGHT),
        ("a", Action.MOVE_LEFT),
        ("q", Action.QUIT),
    ],
)
def test_key_to_action(monkeypatch, terminal_input, key, expected_action):
    monkeypatch.setattr("builtins.input", lambda _: key)
    assert terminal_input.get_action() == expected_action


@pytest.mark.parametrize(
    "key,expected",
    [
        ("g", Action.NONE),
        ("2", Action.NONE),
        ("ss", Action.NONE),
    ],
)
def test_action_none(monkeypatch, terminal_input, key, expected):
    monkeypatch.setattr("builtins.input", lambda _: key)
    assert terminal_input.get_action() == expected
