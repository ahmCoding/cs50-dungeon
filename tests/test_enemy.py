import pytest

from game.core.enemy import Enemy
from game.core.map import Map
from game.core.tile import Tile


@pytest.fixture
def g_map():
    # size of 5*5(x*y)
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.WALL, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map1, (1, 1))


def test_my_turn_to_move_choose_the_valid_move(g_map: Map):
    """the only possible move at position (x=3,y=1) is one step down.
    the position of the Enemy should be (x=3,y=2) after one call of
    Enemy.my_turn_to_move
    """
    for _ in range(100):
        enemy = Enemy(x=3, y=1)
        enemy.my_turn_to_move(g_map)
        assert enemy.get_position() == (3, 2)


def test_my_turn_to_move_surrounded_by_walls(g_map: Map):
    """the only possible move at position (x=1,y=1) is
    to stay at the same position.the position of the Enemy should
    be the same one after x.Times of call on Enemy.my_turn_to_move
    """
    for _ in range(100):
        enemy = Enemy(x=1, y=1)
        enemy.my_turn_to_move(g_map)
        assert enemy.get_position() == (1, 1)


def test_my_turn_to_move_random_map():
    """on a randomly created map(Map.get_map_obj) the player will be moved for
    x.times by calling Enemy.my_turn_to_move . after the calls the position
     of the player should still be a movable one(not a wall)
    """
    for _ in range(100):
        r_map = Map.get_map_obj()
        # set the enemy on start position of the map(safe option for start on map)
        enemy = Enemy(*r_map.get_start_position())
        enemy.my_turn_to_move(r_map)
        assert r_map.is_movable(*enemy.get_position())
