import random

from game.core.character import Character
from game.core.map import Map
from game.core.weapon import Weapon


class Enemy(Character):
    @classmethod
    def get_enemy_obj(cls, x: int = 0, y: int = 0, c_weapon: Weapon | None = None):
        """function to create an Enemy object / factory
        :param x: x position of the character / width
        :param y: y position of the character / height
        :param c_weapon: weapon of the character
        """

        if c_weapon is None:
            c_weapon = Weapon()
        return cls(x=x, y=y, weapon=c_weapon)

    def my_turn_to_move(self, g_map: Map):
        """function to move the Enemy-object
        the direction of the move is based on a randomly chosen direction between the
        free fields with distance of one to the current position of the Enemy-Obj
        g_map: Map object
        """
        # find the moveable Direction
        moveable_dirs = [
            direct
            for direct in Character.Direction
            if g_map.is_movable(*self.next_position(direct))
        ]
        if moveable_dirs:
            self.move(random.choice(moveable_dirs))
