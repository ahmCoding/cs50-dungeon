import pytest

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
    return Map().get_map_obj_from_grid(map1, (1, 2))


def test_injected_map_size(g_map: Map) -> None:
    assert g_map.get_map_size() == (5, 5)


def test_get_start_pos(g_map: Map) -> None:
    assert g_map.get_start_position() == (1, 2)
