import pytest
from game.Player import Player

@pytest.fixture
def player():
    return Player()

def test_player_move_up(player: Player):
    x_old,y_old= player.x, player.y
    player.move(Player.Direction.UP)
    assert player.x == x_old
    assert player.y < y_old

def test_player_move_down(player: Player):
    x_old,y_old= player.x, player.y
    player.move(Player.Direction.DOWN)
    assert player.x == x_old
    assert player.y > y_old

def test_player_move_left(player: Player):
    x_old,y_old= player.x, player.y
    player.move(Player.Direction.LEFT)
    assert player.x < x_old
    assert player.y == y_old

def test_player_move_right(player: Player):
    x_old,y_old= player.x, player.y
    player.move(Player.Direction.RIGHT)
    assert player.x > x_old
    assert player.y == y_old

def test_player_next_up(player: Player):
    new_x,new_y= player.next_position(Player.Direction.UP)
    assert  player.x == new_x
    assert  player.y > new_y

def test_player_next_down(player: Player):
    new_x,new_y= player.next_position(Player.Direction.DOWN)
    assert  player.x == new_x
    assert  player.y < new_y

def test_player_next_left(player: Player):
    new_x,new_y= player.next_position(Player.Direction.LEFT)
    assert  player.x > new_x
    assert  player.y == new_y

def test_player_next_right(player: Player):
    new_x,new_y= player.next_position(Player.Direction.RIGHT)
    assert  player.x < new_x
    assert  player.y == new_y