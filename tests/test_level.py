import pytest

from game.core.level import Level
from game.core.map import Map
from game.core.player import Player
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


@pytest.fixture
def player():
    return Player.get_player_obj(
        1, 1
    )  # player should start from a point in the map, which is not a wall


def test_number_of_enemies(g_map: Map) -> None:
    l1 = Level.get_level_object(g_map, 3)
    assert len(l1.get_enemies()) == 3


def test_no_enemies(g_map: Map) -> None:
    l1 = Level.get_level_object(g_map, 0)
    assert len(l1.get_enemies()) == 0


def test_enemies_pos(g_map: Map) -> None:
    """if the enemies exists in expected fields of the map"""
    l1 = Level.get_level_object(g_map, 3)
    free_poses = g_map.get_free_map_positions()
    for enemy in l1.get_enemies():
        assert enemy.get_position() in free_poses


def test_find_enemy(g_map: Map) -> None:
    """if the created and positioned enemy is found"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    e1.set_position(2, 1)
    assert l1.find_enemy_at_position((2, 1)) == e1


def test_find_no_enemy(g_map: Map) -> None:
    """if the created and positioned enemy is not found in a wrong position"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    e1.set_position(2, 1)
    assert l1.find_enemy_at_position((3, 1)) is None


def test_attack_at(g_map, player: Player) -> None:
    """if a created , positioned and attacked enemy has the right health points"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    e1.set_position(2, 1)
    hp_before_attack = e1.get_hp()
    num_attacks = 3
    for _ in range(num_attacks):
        l1.attack_at((2, 1), player)

    assert e1.get_hp() == hp_before_attack - num_attacks


def test_attack_at_enemy_elimination_from_level(g_map: Map, player: Player) -> None:
    """if dead enemy (Enemy.get_hp() < 0 ) will be eliminated from the level"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    e1.set_position(2, 1)
    num_attacks = e1.get_hp()
    for _ in range(num_attacks):
        l1.attack_at((2, 1), player)
    # the list of enemies should be empty for the level
    assert not l1.get_enemies()


def test_attack_player(g_map: Map, player: Player) -> None:
    """if a player will be attacked by enemies of a level"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    enemy_pos = (2, 1)
    e1.set_position(*enemy_pos)
    enemy_get_pos_before_attack = e1.get_position()
    player_pos = (1, 1)
    player.set_position(*player_pos)  # left to the enemy
    player_hp_before_attack = player.get_hp()
    num_attacks = 3
    for _ in range(num_attacks):
        l1.move_enemies(player)
    assert player.get_hp() == player_hp_before_attack - num_attacks
    assert e1.get_position() == enemy_get_pos_before_attack
