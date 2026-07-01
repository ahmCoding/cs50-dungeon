import random

from game.core.enemy import Enemy
from game.core.map import Map


class Level:
    def __init__(self, g_map: Map, enemies: list[Enemy]) -> None:
        self._g_map = g_map
        self._enemies = enemies

    @classmethod
    def get_level_object(cls, g_map: Map, enemy_counts: int):
        """function to create a Level object / factory
        :param g_map: game map
        :param enemy_counts: number of enemies on the map
        :return: Level object
        """
        created_enemies = 0
        free_pos_of_map = g_map.get_free_map_positions()
        enemies: list[Enemy] = []
        if free_pos_of_map:
            while enemy_counts > created_enemies and free_pos_of_map:
                pos = random.choice(list(free_pos_of_map))
                free_pos_of_map.remove(pos)
                enemies.append(Enemy(*pos))
                created_enemies += 1

        return cls(g_map, enemies)

    def get_enemies(self) -> list[Enemy]:
        return self._enemies
