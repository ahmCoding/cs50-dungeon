from enum import Enum


class Player:
    """
    this class represents a player in the game
    """

    class Direction(Enum):
        """
        The Enum representing the direction of the player.
        the first element of the tuple represents the x value for horizontal movement
        the second element represents the y value for vertical movement
        """

        UP = (0, -1)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        RIGHT = (1, 0)

    def __init__(self, x: int = 0, y: int = 0):
        """
        :param x: width
        :param y: height
        """
        self.x = x
        self.y = y

    def move(self, direction: Direction):
        dx, dy = direction.value
        self.x += dx
        self.y += dy

    def next_position(self, direction: Direction) -> tuple[int, int]:
        dx, dy = direction.value
        return self.x + dx, self.y + dy
