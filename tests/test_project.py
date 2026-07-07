import pytest

from game.core.dungeon import Dungeon
from game.core.level import Level
from game.core.map import Map
from game.core.player import Player
from game.core.tile import Tile
from game.input.action import Action
from game.input.scripted import ScriptedInput
from game.render.null import NullRenderer
from game.render.terminal import TerminalRenderer
from project import execute_action, is_won, play


@pytest.fixture
def g_map1():
    map1 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map1, (1, 1))


@pytest.fixture
def g_map2():
    map2 = [
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
        [Tile.WALL, Tile.WALL, Tile.WALL, Tile.STAIRS, Tile.WALL],
    ]
    return Map.get_map_obj_from_grid(map2, (1, 1))


@pytest.fixture
def g_level1(g_map1):
    level = Level.get_level_object(g_map1)
    # set the positon of default created enemy on (0,0) to create
    # a deterministic range to move the player and test the movement logic
    level.get_enemies()[0].set_position(0, 0)
    return level


@pytest.fixture
def g_level2(g_map2):
    level = Level.get_level_object(g_map2)
    # set the positon of default created enemy on (0,0) to create
    # a deterministic range to move the player and test the movement logic
    level.get_enemies()[0].set_position(0, 0)
    return level


@pytest.fixture
def g_dungeon(g_level1: Level, g_level2: Level):
    return Dungeon([g_level1, g_level2])


@pytest.fixture
def player():
    return Player.get_player_obj(
        1, 1
    )  # player should start from a point in the map, which is not a wall


@pytest.fixture
def t_renderer():
    return TerminalRenderer()


def test_move_to_right_wall(g_dungeon: Dungeon, player: Player):
    m_width, _ = g_dungeon.get_current_level().get_map().get_map_size()
    for x in range(m_width):
        execute_action(g_dungeon, player, Player.Direction.RIGHT)
    assert (
        player.x == m_width - 2
    )  # range from 0 to m_width-1 and subtraction -1 for the wall


def test_move_to_left_wall(g_dungeon: Dungeon, player: Player):
    m_width, _ = g_dungeon.get_current_level().get_map().get_map_size()
    for x in range(m_width):
        execute_action(g_dungeon, player, Player.Direction.LEFT)
    assert player.x == 1  # left wall x=0 , so the player is allowed only to x=1


def test_move_to_upper_wall(g_dungeon: Dungeon, player: Player):
    _, m_height = g_dungeon.get_current_level().get_map().get_map_size()
    for y in range(m_height):
        execute_action(g_dungeon, player, Player.Direction.UP)
    assert player.y == 1


def test_move_to_lower_wall(g_dungeon: Dungeon, player: Player):
    _, m_height = g_dungeon.get_current_level().get_map().get_map_size()
    for y in range(m_height):
        execute_action(g_dungeon, player, Player.Direction.DOWN)
    assert player.y == m_height - 2


def test_player_on_stairs_game_not_won(g_dungeon: Dungeon):
    """we set the player on the stairs of the first Map"""
    p1 = Player.get_player_obj(2, 2)
    assert not is_won(g_dungeon, p1)


def test_player_game_not_won(g_dungeon: Dungeon):
    """we set the player in the second Map on a normal field"""
    g_dungeon.next_level()
    p1 = Player.get_player_obj(2, 0)
    assert not is_won(g_dungeon, p1)


def test_is_won_true(g_dungeon: Dungeon):
    """we set the player on the wining coordinate, second map x=3,y=4"""
    g_dungeon.next_level()
    p1 = Player.get_player_obj(3, 4)
    assert is_won(g_dungeon, p1)


def test_render_player(g_map1: Map, player: Player, t_renderer: TerminalRenderer):
    str_map = t_renderer.to_string(g_map1, [player])
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # player is as defined in @pytest.fixture for player in coordinate x=1,y=1.
    # Here we test the position for the valid char
    assert tmp_map[1][1] == TerminalRenderer.CHARACTER_TO_CHAR[type(player)]


def test_render_field(g_map1: Map, player: Player, t_renderer: TerminalRenderer):
    str_map = t_renderer.to_string(g_map1, [player])
    tmp_map = [row for row in str_map.split("\n") if row != ""]
    # as defined in @pytest.fixture for g_map1,the map contains x=2,y=2: ">"
    # and x=3,y=3: "." . we simply compare the render version with the original map
    assert tmp_map[2][2] == TerminalRenderer.tile_to_char(g_map1.get_tile(2, 2))
    assert tmp_map[3][3] == TerminalRenderer.tile_to_char(g_map1.get_tile(3, 3))


def test_execute_action_attack(g_dungeon: Dungeon, player: Player):
    """if the move action is interpreted right,
    when on the directed field is an enemy"""

    enemy = g_dungeon.get_current_level().get_enemies()[
        0
    ]  # there is only one enemy in the level
    enemy_pos = (1, 1)
    player_pos = (2, 1)  # right to the enemy
    enemy.set_position(*enemy_pos)
    enemy_old_hp = enemy.get_hp()
    player.set_position(*player_pos)
    count_move = 1
    for _ in range(count_move):
        execute_action(g_dungeon, player, Player.Direction.LEFT)

    assert player.get_position() == player_pos  # right pos
    assert enemy.get_hp() == enemy_old_hp - count_move  # right hp of enemy after attack


def test_execute_action_move(g_dungeon: Dungeon, player: Player):
    """if the move action is interpreted right,
    when the directed field is free"""

    enemy = g_dungeon.get_current_level().get_enemies()[
        0
    ]  # there is only one enemy in the level
    enemy_pos = (1, 1)
    player_pos = (2, 1)  # right to the enemy
    enemy.set_position(*enemy_pos)
    enemy_old_hp = enemy.get_hp()
    player.set_position(*player_pos)
    count_move = 1
    for _ in range(count_move):
        execute_action(g_dungeon, player, Player.Direction.RIGHT)

    assert player.get_position() != player_pos  # right pos
    assert enemy.get_hp() == enemy_old_hp  # right hp of enemy after attack


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
