from enum import Enum, auto


class Tile(Enum):
    """
    this class represents a tile on the map
    """

    WALL = auto()
    FIELD = auto()
    STAIRS = auto()
