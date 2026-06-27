import pytest

from game.core.dungeon import Dungeon
from game.core.map import Map
from game.core.tile import Tile

"""
In some of tests we are comparing Map-objects with help of '==' operator.
This operator is not defined in Map-class , but the default behaviour ('is')
is sufficient for us. 
"""


@pytest.fixture
def g_map1():
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map1, (1, 1))


@pytest.fixture
def g_map2():
    map2 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map2, (1, 1))


@pytest.fixture
def g_dungeon(g_map1: Map, g_map2: Map):
    return Dungeon([g_map1, g_map2])


def test_get_current_map_after_start(g_dungeon: Dungeon, g_map1: Map):
    """after start  the current map should be the first one is"""
    assert g_dungeon.get_current_map() == g_map1


def test_next_map(g_dungeon: Dungeon, g_map2: Map):
    """after calling obj.next_map() for one time, the second map should be
    the current one"""
    g_dungeon.next_map()
    assert g_dungeon.get_current_map() == g_map2


def test_is_last_map_false(g_dungeon: Dungeon):
    """after start the current map should not be the last one"""
    assert not g_dungeon.is_last_map()


def test_is_last_map_true(g_dungeon: Dungeon, g_map2: Map):
    """after calling obj.next_map() for one time, the second map should be
    the last one"""
    g_dungeon.next_map()
    assert g_dungeon.is_last_map()


def test_next_map_extreme(g_dungeon: Dungeon, g_map2: Map):
    """after start and calling obj.next_map() for x.times (x>1) of ,
    the current map should still be the second one. even though the
    obj.next_map() was called more the once
    """
    g_dungeon.next_map()
    g_dungeon.next_map()
    g_dungeon.next_map()
    assert g_dungeon.get_current_map() == g_map2
