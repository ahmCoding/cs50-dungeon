import random

from game.core.tile import Tile


class Map:
    """
    this class represents a map in the game
    """

    def __init__(
        self,
        grid: list[list[Tile]],
        w: int,
        h: int,
        start_position: tuple[int, int],
        stairs_position: tuple[int, int],
    ):
        """
        :param grid: 2d grid of Tile-Objects /game map
        :param w: width of the grid /x
        :param h: height of the grid /y
        :param start_position: x and y coordinates of the grid's start point ,
            here will be the player placed at the start
        :param stairs_position: x and y coordinates of the stairs position
        """
        self._height = h
        self._width = w
        self._map = grid
        self._stairs_tile = Tile.STAIRS
        self._start_position = start_position
        self._stairs_position = stairs_position

    @staticmethod
    def _create_2d_tile_grid(
        width: int, height: int, start_position: tuple[int, int]
    ) -> tuple[list[list[Tile]], tuple[int, int]]:
        """
        this function creates a 2d grid of Tile-Objects.
        the position of the stairs on the grid will be chosen randomly
        :return: a tuple , which contains a 2d grid of Tile-Objects and the position
        of the stairs on the grid in (x,y) format
        """
        while True:
            r_x = random.randint(1, width - 2)  # random x-pos for stairs
            r_y = random.randint(1, height - 2)  # random y-pos for stairs
            if (r_x, r_y) != start_position:  # no stairs at map start pos
                break

        stairs_position = (r_x, r_y)  # save the stairs pos

        tile_grid = [[Tile.WALL for w in range(width)] for h in range(height)]
        # only write somewhere in the middle of field
        for h in range(1, height - 1):
            for w in range(1, width - 1):
                if h == r_y and w == r_x:
                    tile_grid[h][w] = Tile.STAIRS
                else:
                    tile_grid[h][w] = Tile.FIELD
        return tile_grid, stairs_position

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
        :return: an object of the Map-Class
        """
        grid, stairs_pos = cls._create_2d_tile_grid(w, h, start_position)
        tmp_obj = cls(grid, w, h, start_position, stairs_pos)

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
        :return: an object of the Map-Class
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
        assert stairs_pos is not None  # there muss be a stairs in the gird
        # grid width and height
        grid_h = len(grid)
        grid_w = len(grid[0])
        tmp_obj = cls(
            grid=grid,
            w=grid_w,
            h=grid_h,
            start_position=start_position,
            stairs_position=stairs_pos,
        )
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
