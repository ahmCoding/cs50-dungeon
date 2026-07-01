import pytest

from game.core.level import Level
from game.core.map import Map
from game.core.tile import Tile


@pytest.fixture
def g_map():
    # size of 5*5(x*y)
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map1, (1, 2))


def test_number_of_enemies(g_map: Map) -> None:
    l1 = Level.get_level_object(g_map, 3)
    assert len(l1.get_enemies()) == 3


def test_no_enemies(g_map: Map) -> None:
    l1 = Level.get_level_object(g_map, 0)
    assert len(l1.get_enemies()) == 0
