import random

from game.core.character import Character
from game.core.map import Map


class Enemy(Character):
    def my_turn_to_move(self, g_map: Map):
        """function to move the Enemy-object
        the direction of the move is based on a randomly chosen direction between the
        free field with distance of one to the current position of the
        g_map: Map object
        """
        # find the moveable Direction
        moveable_dirs = [
            direct
            for direct in Character.Direction
            if g_map.is_movable(*self.next_position(direct))
        ]
        self.move(random.choice(moveable_dirs))


def main():
    map1 = Map.get_map_obj()
    e1 = Enemy(*map1.get_start_position())
    e1.my_turn_to_move(map1)


if __name__ == "__main__":
    main()
