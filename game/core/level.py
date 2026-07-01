import random

from game.core.enemy import Enemy
from game.core.map import Map


class Level:
    def __init__(self, g_map: Map, enemies: list[Enemy]) -> None:
        self._g_map = g_map
        self._enemies = enemies

    @classmethod
    def get_level_object(cls, g_map: Map, enemy_count: int):
        """function to create a Level object / factory
        :param g_map: game map
        :param enemy_count: number of enemies on the map, if this number is greater than
         the number of free slots on the map, the number of free slots will be taken
        :return: Level object
        """
        list_free_pos_of_map = list(g_map.get_free_map_positions())
        try:
            random_free_pos_of_map = random.sample(list_free_pos_of_map, enemy_count)
        except ValueError:  # if enemy_count > free slots of the map
            random_free_pos_of_map = random.sample(
                list_free_pos_of_map, len(list_free_pos_of_map)
            )

        enemies: list[Enemy] = []
        for r_pos in enumerate(random_free_pos_of_map):
            enemies.append(Enemy(*r_pos))

        return cls(g_map, enemies)

    def get_enemies(self) -> list[Enemy]:
        return self._enemies
