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


def test_get_stairs_pos(g_map: Map) -> None:
    """if the Map.get_map_obj_from_grid find the stairs in the uploaded grid"""
    # the stairs pos in  the map1 grid is (x=2,y=2)
    assert g_map.get_stairs_position() == (2, 2)


def test_stairs_pos_and_start_pos() -> None:
    """if the stairs_position and start_position are different"""
    for _ in range(100):
        my_map = Map().get_map_obj()
        assert my_map.get_stairs_position() != my_map.get_start_position()
