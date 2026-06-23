from game.Map import Map
from game.Player import Player
from game.Tile import Tile


def render(g_map: Map, player: Player) -> str:
    rendered_map_as_list = from_tils_to_string_list(g_map.get_game_map())
    rendered_map_as_list[player.y][player.x] = player.char
    return from_string_list_to_string(rendered_map_as_list)


def move(g_map: Map, player: Player, key: str):
    match key:
        case "s":
            direction = Player.Direction.DOWN
        case "a":
            direction = Player.Direction.LEFT
        case "d":
            direction = Player.Direction.RIGHT
        case "w":
            direction = Player.Direction.UP
        case _:
            return
    new_x, new_y = player.next_position(direction)
    if g_map.is_movable(new_x, new_y):
        player.move(direction)


def check_win(g_map: Map, player: Player) -> bool:
    return g_map.get_tile(player.x, player.y) == g_map.get_win_tile()


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
    map_dict = {"WALL": "#", "STAIRS": ">", "FIELD": "."}
    return map_dict[str(tile)]


def from_tils_to_string_list(tils_list: list[list[Tile]]):
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


def main():
    # mt = [
    #     [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    #     [Tile.WALL, Tile.FIELD, Tile.FIELD, Tile.FIELD, Tile.WALL],
    #     [Tile.WALL, Tile.FIELD, Tile.STAIRS, Tile.FIELD, Tile.WALL],
    #     [Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL, Tile.WALL],
    # ]
    # my_map = Map.get_map_obj_from_grid(mt)
    # tst = from_tils_to_string_list(mt)
    # print(from_string_list_to_string(tst))

    print("w: up , s: down , a: left, d: right, :q for quit")
    g_map = Map.get_map_obj(12, 8)
    player = Player(1, 1)
    while True:
        print(render(g_map, player))
        if check_win(g_map, player):
            print("*" * 9 + " Game Won  " + "*" * 9)
            break
        user_i = input("enter your choice: ")
        if user_i == ":q":
            break
        move(g_map, player, user_i)


if __name__ == "__main__":
    main()
