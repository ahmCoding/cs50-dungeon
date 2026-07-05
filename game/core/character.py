from enum import Enum

from game.core.weapon import Weapon


class Character:
    """
    this class represents a character in the game
    """

    class Direction(Enum):
        """
        The Enum representing the direction of the character.
        the first element of the tuple represents the x value for horizontal movement
        the second element represents the y value for vertical movement
        """

        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)

    MAX_HP = 10

    def __init__(self, x: int, y: int, weapon: Weapon) -> None:
        """
        :param x: x position of the character / width
        :param y: y position of the character / height
        :param weapon: weapon of the character
        """
        self.x = x
        self.y = y
        self.weapon = weapon
        self.hp: int = self.MAX_HP

    def move(self, direction: Direction):
        """
        function that moves the character according to the given direction
        :param direction:
        :return:
        """
        dx, dy = direction.value
        self.x += dx
        self.y += dy

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> tuple[int, int]:
        """
        :return: (x, y)
        """
        return self.x, self.y

    def next_position(self, direction: Direction) -> tuple[int, int]:
        """This function returns the next position in the game based in the given
        direction This is only a new calculated position, the Player is not moved to
         the direction
        """
        dx, dy = direction.value
        return self.x + dx, self.y + dy

    def take_damage(self, amount: int) -> None:
        """function to reduce the health points of the character"""
        self.hp -= amount

    def get_hp(self) -> int:
        """function to return the current health points of the character"""
        return self.hp

    def get_weapon_damage(self) -> int:
        """function to get the damage power of the character"""
        return self.weapon.get_damage()
