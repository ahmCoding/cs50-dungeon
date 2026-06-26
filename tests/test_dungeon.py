import pytest

from game.core.dungeon import Dungeon
from game.core.map import Map
from game.core.tile import Tile


@pytest.fixture
def g_map1():
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map().get_map_obj_from_grid(map1)


@pytest.fixture
def g_map2():
    map2 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map().get_map_obj_from_grid(map2)


@pytest.fixture
def g_dungeon(g_map1: Map, g_map2: Map):
    return Dungeon([g_map1, g_map2])


def test_first_map_after_start(g_dungeon: Dungeon, g_map1: Map):
    """2 maps in dungeon obj, current map ist the first one"""
    assert g_dungeon.get_current_map() == g_map1


def test_next_map(g_dungeon: Dungeon, g_map2: Map):
    """2 maps in dungeon obj, current map ist the first one,
    after 1.time obj.next_map() call, the current map should be
    the second one"""
    g_dungeon.next_map()
    assert g_dungeon.get_current_map() == g_map2


def test_is_last_map_after_start(g_dungeon: Dungeon):
    """2 maps in dungeon obj, current map ist the first one"""
    assert not g_dungeon.is_last_map()


def test_is_last_map(g_dungeon: Dungeon, g_map2: Map):
    """2 maps in dungeon obj, current map ist the first one
    after 1.time of obj.next_map() call, the current map should
    still be the last one
    """
    g_dungeon.next_map()
    assert g_dungeon.is_last_map()


def test_is_next_map(g_dungeon: Dungeon, g_map2: Map):
    """2 maps in dungeon obj, current map ist the first one
    after x.times (x>1) of obj.next_map() call, the current map should
    still be the second one
    """
    g_dungeon.next_map()
    g_dungeon.next_map()
    g_dungeon.next_map()
    assert g_dungeon.get_current_map() == g_map2
