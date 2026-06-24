import random
from typing import Self

from game.core.Tile import Tile


class Map:
    def __init__(self, w: int = 5, h: int = 5):
        """
        :param w: width of the map /x
        :param h: height of the map /y
        """
        self._height = h
        self._width = w
        self._map = []
        self._win_tile = Tile.STAIRS

    def _create_map(self):
        r_x = random.randint(1, self._width - 2)
        r_y = random.randint(1, self._height - 2)

        tmp_map = [[Tile.WALL for w in range(self._width)] for h in range(self._height)]
        # only write somewhere in the middle of field
        for h in range(1, self._height - 1):
            for w in range(1, self._width - 1):
                if h == r_y and w == r_x:
                    tmp_map[h][w] = Tile.STAIRS
                else:
                    tmp_map[h][w] = Tile.FIELD
        self._map = tmp_map

    @classmethod
    def get_map_obj(cls, w: int = 5, h: int = 5) -> Self:
        tmp_obj = cls(w, h)
        tmp_obj._create_map()
        return tmp_obj

    @classmethod
    def get_map_obj_from_grid(cls, grid: list[list[Tile]]) -> Self:
        tmp_obj = cls()
        tmp_obj._height = len(grid)
        tmp_obj._width = len(grid[0])
        tmp_obj._map = grid
        return tmp_obj

    def is_movable(self, x, y) -> bool:
        return self.get_tile(x, y) != Tile.WALL

    def get_game_map(self) -> list[list[Tile]]:
        return [
            [self.get_tile(x, y) for x in range(self._width)]
            for y in range(self._height)
        ]

    def get_tile(self, x, y) -> Tile:
        """
        :param x: x coordinate of the tile
        :param y: y coordinate of the tile
        :return:  as a string
        if the x and y are not in the map, the wall character will be returned.
        """
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._map[y][x]
        return Tile.WALL

    def get_win_tile(self) -> Tile:
        return self._win_tile

    def get_map_size(self) -> tuple[int, int]:
        """
        :return: width and height of the map as a tuple
        """
        return self._width, self._height
