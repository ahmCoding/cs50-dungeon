from game.core.Map import Map
from game.core.Player import Player
from game.render.utils import render


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


def main():
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
