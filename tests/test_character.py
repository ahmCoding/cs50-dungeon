import pytest

from game.core.character import Character


@pytest.fixture
def player():
    return Character()


def test_player_move_up(player: Character):
    x_old, y_old = player.x, player.y
    player.move(Character.Direction.UP)
    assert player.x == x_old
    assert player.y < y_old


def test_player_move_down(player: Character):
    x_old, y_old = player.x, player.y
    player.move(Character.Direction.DOWN)
    assert player.x == x_old
    assert player.y > y_old


def test_player_move_left(player: Character):
    x_old, y_old = player.x, player.y
    player.move(Character.Direction.LEFT)
    assert player.x < x_old
    assert player.y == y_old


def test_player_move_right(player: Character):
    x_old, y_old = player.x, player.y
    player.move(Character.Direction.RIGHT)
    assert player.x > x_old
    assert player.y == y_old


def test_player_next_up(player: Character):
    new_x, new_y = player.next_position(Character.Direction.UP)
    assert player.x == new_x
    assert player.y > new_y


def test_player_next_down(player: Character):
    new_x, new_y = player.next_position(Character.Direction.DOWN)
    assert player.x == new_x
    assert player.y < new_y


def test_player_next_left(player: Character):
    new_x, new_y = player.next_position(Character.Direction.LEFT)
    assert player.x > new_x
    assert player.y == new_y


def test_player_next_right(player: Character):
    new_x, new_y = player.next_position(Character.Direction.RIGHT)
    assert player.x < new_x
    assert player.y == new_y


def test_player_set_pose(player: Character):
    assert player.get_position() == (0, 0)  # default pos
    player.set_position(2, 4)
    assert player.get_position() == (2, 4)
