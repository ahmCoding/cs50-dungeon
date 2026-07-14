import random

from game.core.character import Character
from game.core.enemy import Enemy
from game.core.map import Map


class Level:
    def __init__(self, g_map: Map, enemies: list[Enemy]) -> None:
        self._g_map = g_map
        self._enemies = enemies

    def _remove_enemy_if_dead(self, enemy: Enemy) -> None:
        """function to remove an enemy form the level, if it is dead
        the caller granite that the enemy exists in the level"""
        if enemy.get_hp() <= 0:
            self._enemies.remove(enemy)

    @classmethod
    def get_level_object(cls, g_map: Map, enemy_count: int = 1):
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
        for r_pos in random_free_pos_of_map:
            enemies.append(Enemy.get_enemy_obj(*r_pos))

        return cls(g_map, enemies)

    def get_enemies(self) -> list[Enemy]:
        """
        :return: list of enemies
        """
        return self._enemies

    def get_map(self) -> Map:
        """function to get the map of current level
        :return: Map
        """
        return self._g_map

    def move_enemies(self, other_character: Character) -> None:
        """
        function to move enemies of the current level.
        if a character(player) is in reachable distance ,
        it will be attacked instead of movement. see @Enemy.my_turn_to_move

        :param other_character: character , which can be attacked
        """
        if self._enemies:
            for enemy in self._enemies:
                enemy.my_turn_to_move(self.get_map(), other_character)

    def find_enemy_at_position(self, pos: tuple[int, int]) -> Enemy | None:
        """function to find and return enemy in a specific position
        :param pos: (x, y) coordinate of the enemy to find
        :return: Enemy if found, else None"""
        for enemy in self._enemies:
            if enemy.get_position() == pos:
                return enemy
        return None

    def attack_at(self, position: tuple[int, int], attacker: Character) -> bool:
        """
        function to execute an attack on a position. if there is an enemy
         at the position, the damage will be applied

        :param position: (x,y) coordinate to check for an enemy
        :param attacker:
        :return: True , of an enemy was found and damaged , else False
        """
        if enemy := self.find_enemy_at_position(position):
            enemy.take_damage(attacker.get_weapon_damage())
            self._remove_enemy_if_dead(enemy)
            return True
        return False
