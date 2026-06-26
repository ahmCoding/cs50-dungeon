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
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map().get_map_obj_from_grid(map1, (1, 1))


@pytest.fixture
def g_map2():
    map2 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map().get_map_obj_from_grid(map2, (1, 1))


@pytest.fixture
def g_dungeon(g_map: Map, g_map2: Map):
    return Dungeon([g_map, g_map2])


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


def test_player_on_stairs_game_not_won(g_dungeon: Dungeon):
    """we set the player on the stairs of the first Map"""
    p1 = Player(2, 2)
    assert not is_won(g_dungeon, p1)


def test_player_game_not_won(g_dungeon: Dungeon):
    """we set the player in the second Map on a normal field"""
    g_dungeon.next_map()
    p1 = Player(2, 0)
    assert not is_won(g_dungeon, p1)


def test_is_won_true(g_dungeon: Dungeon):
    """we set the player on the wining coordinate, second map x=3,y=4"""
    g_dungeon.next_map()
    p1 = Player(3, 4)
    assert is_won(g_dungeon, p1)


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
    g_dungeon: Dungeon,
    player: Player,
):
    """
    double move to right , current pos of player is (x:1,y:1) after the double
    right action should be (x:3,y:1)
    """
    scripted_input = ScriptedInput([Action.MOVE_RIGHT, Action.MOVE_RIGHT, Action.QUIT])
    renderer = NullRenderer()
    y_before_actions = player.y
    play(g_dungeon, player, scripted_input, renderer)

    assert player.x == 3 and player.y == y_before_actions
