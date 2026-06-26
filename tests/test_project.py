import pytest

from game.core.dungeon import Dungeon
from game.core.map import Map
from game.core.player import Player
from game.core.tile import Tile
from game.input.action import Action
from game.input.scripted import ScriptedInput
from game.render.null import NullRenderer
from game.render.terminal import TerminalRenderer
from project import is_won, move, play


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


@pytest.fixture
def t_renderer():
    return TerminalRenderer()


def test_move_to_right_wall(g_map: Map, player: Player):
    m_width, _ = g_map.get_map_size()
    for x in range(m_width):
        move(g_map, player, Player.Direction.RIGHT)
    assert (
        player.x == m_width - 2
    )  # range from 0 to m_width-1 and subtraction -1 for the wall


def test_move_to_left_wall(g_map: Map, player: Player):
    m_width, _ = g_map.get_map_size()
    for x in range(m_width):
        move(g_map, player, Player.Direction.LEFT)
    assert player.x == 1  # left wall x=0 , so the player is allowed only to x=1


def test_move_to_upper_wall(g_map: Map, player: Player):
    _, m_height = g_map.get_map_size()
    for y in range(m_height):
        move(g_map, player, Player.Direction.UP)
    assert player.y == 1


def test_move_to_lower_wall(g_map: Map, player: Player):
    _, m_height = g_map.get_map_size()
    for y in range(m_height):
        move(g_map, player, Player.Direction.DOWN)
    assert player.y == m_height - 2


def test_check_win_false(g_map: Map):
    p1 = Player(
        1, 2
    )  # set the player at the coordinate x=1,y=2 , where we have a "." on the map
    g_dungeon = Dungeon([g_map])
    assert not (is_won(g_dungeon, p1))


def test_check_win_true(g_map: Map):
    p1 = Player(2, 2)  # set the player at the wining-coordinate (">")on the map
    g_dungeon = Dungeon([g_map])
    assert is_won(g_dungeon, p1)  # player at coordinate x=2,y=2  like  map tile = ">"


def test_render_player(g_map: Map, player: Player, t_renderer: TerminalRenderer):
    str_map = t_renderer.to_string(g_map, player)
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # player is as defined in @pytest.fixture for player in coordinate x=1,y=1.
    # Here we test the position for the valid char
    assert tmp_map[1][1] == TerminalRenderer.PLAYER_CHAR


def test_render_field(g_map: Map, player: Player, t_renderer: TerminalRenderer):
    str_map = t_renderer.to_string(g_map, player)
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # as defined in @pytest.fixture for g_map,the map contains x=2,y=2: ">"
    # and x=3,y=3: "." . we simply compare the render version with the original map
    assert tmp_map[2][2] == TerminalRenderer.tile_to_char(g_map.get_tile(2, 2))
    assert tmp_map[3][3] == TerminalRenderer.tile_to_char(g_map.get_tile(3, 3))


def test_play(
    g_map: Map,
    player: Player,
):
    """
    double move to right , current pos of player is (x:1,y:1) after the double
    right action should be (x:3,y:1)
    """
    g_dungeon = Dungeon([g_map])
    scripted_input = ScriptedInput([Action.MOVE_RIGHT, Action.MOVE_RIGHT, Action.QUIT])
    renderer = NullRenderer()
    y_before_actions = player.y
    play(g_dungeon, player, scripted_input, renderer)

    assert player.x == 3 and player.y == y_before_actions
