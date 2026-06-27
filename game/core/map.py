import random

from game.core.tile import Tile


class Map:
    """
    this class represents a map in the game
    """

    def __init__(
        self,
        w: int = 5,
        h: int = 5,
        start_position: tuple[int, int] = (1, 1),
        stairs_position: tuple[int, int] | None = None,
    ):
        """
        :param w: width of the map /x
        :param h: height of the map /y
        :param start_position: x and y coordinates of the map start,
            here will be the player placed at the start of the map
        :param stairs_position: x and y coordinates of the stairs position,
        None is a transient state and will be set immediately by factory methods
        """
        self._height = h
        self._width = w
        self._map = list[list[Tile]]
        self._stairs_tile = Tile.STAIRS
        self._stairs_position: tuple[int, int] | None = stairs_position
        self._start_position = start_position

    def _create_map(self):
        """
        this function creates the map. a map object consts of Tile-Objects
        the position of the stairs on the map will be chosen randomly
        """
        while True:
            r_x = random.randint(1, self._width - 2)  # random x-pos for stairs
            r_y = random.randint(1, self._height - 2)  # random y-pos for stairs
            if (r_x, r_y) != self._start_position:  # no stairs at map start pos
                break

        self._stairs_position = (r_x, r_y)  # save the stairs pos

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
    def get_map_obj(
        cls, w: int = 5, h: int = 5, start_position: tuple[int, int] = (1, 1)
    ):
        """
        standard function to create the map / factory method
        :param w: width of the map /x
        :param h: height of the map /y
        :param start_position: x and y coordinates of the start,
        here will be the player placed at the start of the map
        :return: a map object
        """
        tmp_obj = cls(w, h, start_position)
        tmp_obj._create_map()
        return tmp_obj

    @classmethod
    def get_map_obj_from_grid(
        cls, grid: list[list[Tile]], start_position: tuple[int, int]
    ):
        """
        standard function to create the map from a grid / factory method
        :param grid: a 2d grid of tiles
        :param start_position: x and y coordinates of the start,
        here will be the player placed at the start of the map
        :return: a map object
        """

        # find the position of the first stairs in uploaded grid
        stairs_pos = None
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                if tile == Tile.STAIRS:
                    stairs_pos = (x, y)
                    break
            if stairs_pos is not None:
                break

        tmp_obj = cls(start_position=start_position, stairs_position=stairs_pos)
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

    def get_stairs_tile(self) -> Tile:
        return self._stairs_tile

    def get_map_size(self) -> tuple[int, int]:
        """
        :return: width and height of the map as a tuple
        """
        return self._width, self._height

    def get_start_position(self) -> tuple[int, int]:
        """
        :return: the starting position of the map as a tuple
        in format of (x, y)
        """
        return self._start_position

    def get_stairs_position(self) -> tuple[int, int]:
        """
        :return: the stairs position of the map as a tuple
        in format of (x, y)
        """
        assert self._stairs_position is not None
        return self._stairs_position
