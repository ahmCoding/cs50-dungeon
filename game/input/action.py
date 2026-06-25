from enum import Enum, auto


class Action(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    NONE = auto()
    QUIT = auto()
