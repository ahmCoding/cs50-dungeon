import pytest

from game.core.dungeon import Dungeon
from game.core.level import Level, Map
from game.core.tile import Tile

"""
In some of tests we are comparing Map-objects with help of '==' operator.
This operator is not defined in Map-class , but the default behaviour ('is')
is sufficient for us. 
"""


@pytest.fixture
def g_level1():
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map1, (1, 1))


@pytest.fixture
def g_level2():
    map2 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map2, (1, 1))


@pytest.fixture
def g_map1(g_level1):
    return Level.get_level_object(g_level1)


@pytest.fixture
def g_map2(g_level2):
    return Level.get_level_object(g_level2)


@pytest.fixture
def g_dungeon(g_level1: Level, g_level2: Level):
    return Dungeon([g_level1, g_level2])


def test_get_current_level_after_start(g_dungeon: Dungeon, g_level1: Level):
    """after start  the current level should be the first one is"""
    assert g_dungeon.get_current_level() == g_level1


def test_next_level(g_dungeon: Dungeon, g_level2: Level):
    """after calling obj.next_level() for one time, the second level should be
    the current one"""
    g_dungeon.next_level()
    assert g_dungeon.get_current_level() == g_level2


def test_is_last_level_false(g_dungeon: Dungeon):
    """after start the current level should not be the last one"""
    assert not g_dungeon.is_last_level()


def test_is_last_level_true(g_dungeon: Dungeon, g_level2: Map):
    """after calling obj.next_level() for one time, the second level should be
    the last one"""
    g_dungeon.next_level()
    assert g_dungeon.is_last_level()


def test_next_level_extreme(g_dungeon: Dungeon, g_level2: Map):
    """after start and calling obj.next_level() for x.times (x>1) of ,
    the current level should still be the second one. even though the
    obj.next_level() was called more the once
    """
    g_dungeon.next_level()
    g_dungeon.next_level()
    g_dungeon.next_level()
    assert g_dungeon.get_current_level() == g_level2
