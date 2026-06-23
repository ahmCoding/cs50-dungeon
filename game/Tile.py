from enum import Enum, auto


class Tile(Enum):
    WALL = auto()
    FIELD = auto()
    STAIRS = auto()

    def __str__(self):
        return self.name
