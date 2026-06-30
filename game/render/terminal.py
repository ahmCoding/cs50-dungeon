from game.core.character import Character
from game.core.enemy import Enemy
from game.core.map import Map
from game.core.player import Player
from game.core.tile import Tile
from game.render.base import Renderer


class TerminalRenderer(Renderer):
    TILE_TO_CHAR = {Tile.WALL: "#", Tile.STAIRS: ">", Tile.FIELD: "."}
    CHARACTER_TO_CHAR: dict[type[Character], str] = {
        Player: "@",
        Enemy: "&",
    }  # temporary char for the player

    def draw(self, g_map: Map, characters: list[Character]) -> None:
        print(self.to_string(g_map, characters))

    def to_string(self, g_map: Map, characters: list[Character]) -> str:
        rendered_map_as_list = self._from_tiles_to_string_list(g_map.get_game_map())
        for character in characters:
            rendered_map_as_list[character.y][character.x] = self.CHARACTER_TO_CHAR[
                type(character)
            ]
        return self._from_string_list_to_string(rendered_map_as_list)

    @staticmethod
    def _from_string_list_to_string(str_list: list[list[str]]) -> str:
        """
        convert a 2d string list in a  string , which represents the 2d list,
        for each row of the 2d-list there will be a line of text ended with "\n"
        :param str_list: 2d string list
        :return: string representation of the 2d list
        """
        tmp_str = ""
        for row in str_list:
            tmp_str += "".join(row) + "\n"
        return tmp_str

    @classmethod
    def _from_tiles_to_string_list(cls, tils_list: list[list[Tile]]):
        """
        convert a tiles list to a string
        :param tils_list: a 2D list of Tiles
        :return: a string representation of the tiles list
        """
        tmp_map = []
        for tiles in tils_list:
            tmp_map.append(
                [cls.tile_to_char(t) for t in tiles]
            )  # convert from Tile.name to a string list
        return tmp_map

    @classmethod
    def tile_to_char(cls, tile: Tile) -> str:
        """convert a tile to a string with help of a mapping dictionary"""
        return cls.TILE_TO_CHAR[tile]
