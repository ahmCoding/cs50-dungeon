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


def test_attack_at(g_map) -> None:
    """if a created , positioned and attacked enemy has the right health points"""
    l1 = Level.get_level_object(g_map, 1)
    e1 = l1.get_enemies()[0]
    e1.set_position(2, 1)
    # the default hp für every object of Charackter/Enemy/Player ist 10
    # after 3 attacks , there right value for hp is 7
    l1.attack_at((2, 1), 1)
    l1.attack_at((2, 1), 1)
    l1.attack_at((2, 1), 1)
    assert e1.get_hp() == 7
