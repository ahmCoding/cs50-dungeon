import pytest

from game.Map import Map
from game.Player import Player
from project import move


@pytest.fixture
def g_map():
    my_map = [
        ["#", "#", "#", "#", "#"],
        ["#", ".", ".", ".", "#"],
        ["#", ".", ">", ".", "#"],
        ["#", ".", ".", ".", "#"],
        ["#", "#", "#", "#", "#"],
    ]
    my_map = Map.get_map_obj_from_grid(my_map)
    return my_map


@pytest.fixture
def player():
    return Player(
        1, 1
    )  # player should start from a point in the map, which is not a wall


def test_move_to_right_wall(g_map: Map, player: Player):
    m_width, _ = g_map.get_map_size()
    for x in range(m_width):
        move(g_map, player, key="d")
    assert (
        player.x == m_width - 2
    )  # range from 0 to m_width-1 and subtraction -1 for the wall


def test_move_to_left_wall(g_map: Map, player: Player):
    m_width, _ = g_map.get_map_size()
    for x in range(m_width):
        move(g_map, player, key="a")
    assert player.x == 1  # left wall x=0 , so the player is allowed only to x=1


def test_move_to_upper_wall(g_map: Map, player: Player):
    _, m_height = g_map.get_map_size()
    for y in range(m_height):
        move(g_map, player, key="w")
    assert player.y == 1


def test_move_to_lower_wall(g_map: Map, player: Player):
    _, m_height = g_map.get_map_size()
    for y in range(m_height):
        move(g_map, player, key="s")
    assert player.y == m_height - 2
