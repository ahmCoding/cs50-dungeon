from game.core.Map import Map
from game.core.Player import Player
from game.core.Tile import Tile

TILE_TO_CHAR = {Tile.WALL: "#", Tile.STAIRS: ">", Tile.FIELD: "."}
PLAYER_CHAR = "@"  # temporary char for the player


def get_player_char() -> str:
    """function to return a char representing the player for test reasons"""
    return PLAYER_CHAR


def render(g_map: Map, player: Player) -> str:
    rendered_map_as_list = from_tiles_to_string_list(g_map.get_game_map())
    rendered_map_as_list[player.y][player.x] = PLAYER_CHAR
    return from_string_list_to_string(rendered_map_as_list)


def from_string_list_to_string(str_list: list[list[str]]) -> str:
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


def tile_to_char(tile: Tile) -> str:
    """convert a tile to a string with help of a mapping dictionary"""
    return TILE_TO_CHAR[tile]


def from_tiles_to_string_list(tils_list: list[list[Tile]]):
    """
    convert a tiles list to a string
    :param tils_list: a 2D list of Tiles
    :return: a string representation of the tiles list
    """
    tmp_map = []
    for tiles in tils_list:
        tmp_map.append(
            [tile_to_char(t) for t in tiles]
        )  # convert from Tile.name to a string list
    return tmp_map
