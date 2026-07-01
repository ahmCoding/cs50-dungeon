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
    return Map.get_map_obj_from_grid(map1, (1, 2))


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
        my_map = Map.get_map_obj()
        assert my_map.get_stairs_position() != my_map.get_start_position()


def test_number_of_free_positions(g_map: Map) -> None:
    """if the number of free positions on the injected map is correct"""
    # 8 * Tile.Field - 1 (start position) = 7
    free_pos = g_map.get_free_map_positions()
    assert len(free_pos) == 7


def test_start_pos_not_a_free_positions() -> None:
    """the start position of the map should
    never be in the list of free positions"""
    for _ in range(100):
        my_map = Map.get_map_obj()
        free_pos = my_map.get_free_map_positions()
        assert my_map.get_start_position() not in free_pos


def test_stair_pos_not_a_free_positions() -> None:
    """position of the stairs on a map should
    never be in the list of free positions"""
    for _ in range(100):
        my_map = Map.get_map_obj()
        free_pos = my_map.get_free_map_positions()
        assert my_map.get_stairs_position() not in free_pos
