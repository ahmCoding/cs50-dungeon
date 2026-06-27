from enum import Enum, auto


class Action(Enum):
    """
    this class represents a action to be taken in the game
    """

    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    NONE = auto()
    QUIT = auto()
