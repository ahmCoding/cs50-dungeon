import pytest

from game.core.map import Map
from game.core.player import Player
from game.core.tile import Tile
from game.render.terminal import TerminalRender
from project import check_win, move


@pytest.fixture
def g_map():
    my_map = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]  # the win-tile is at coordinate x=2,y=2 , the char is ">"
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


def test_check_win_false(g_map: Map):
    p1 = Player(
        1, 2
    )  # set the player at the coordinate x=1,y=2 , where we have a "." on the map

    assert not (check_win(g_map, p1))


def test_check_win_true(g_map: Map):
    p1 = Player(2, 2)  # set the player at the wining-coordinate (">")on the map
    assert check_win(g_map, p1)  # player at coordinate x=2,y=2  like  map tile = ">"


def test_render_player(g_map: Map, player: Player):
    t_render = TerminalRender()
    str_map = t_render.to_string(g_map, player)
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # player is as defined in @pytest.fixture for player in coordinate x=1,y=1.
    # Here we test the position for the valid char
    assert tmp_map[1][1] == TerminalRender.PLAYER_CHAR


def test_render_field(g_map: Map, player: Player):
    t_render = TerminalRender()
    str_map = t_render.to_string(g_map, player)
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # as defined in @pytest.fixture for g_map,the map contains x=2,y=2: ">"
    # and x=3,y=3: "." . we simply compare the render version with the original map
    assert tmp_map[2][2] == TerminalRender.tile_to_char(g_map.get_tile(2, 2))
    assert tmp_map[3][3] == TerminalRender.tile_to_char(g_map.get_tile(3, 3))
