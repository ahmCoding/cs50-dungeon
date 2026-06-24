from input.action import Action
from input.terminal import TerminalInput

from game.core.map import Map
from game.core.player import Player
from game.render.terminal import TerminalRenderer


def move(g_map: Map, player: Player, p_direction: Player.Direction):
    new_x, new_y = player.next_position(p_direction)
    if g_map.is_movable(new_x, new_y):
        player.move(p_direction)


def check_win(g_map: Map, player: Player) -> bool:
    return g_map.get_tile(player.x, player.y) == g_map.get_win_tile()


# to map ACTION to Player.Direction
ACTION_TO_DIRECTION = {
    Action.MOVE_UP: Player.Direction.UP,
    Action.MOVE_DOWN: Player.Direction.DOWN,
    Action.MOVE_LEFT: Player.Direction.LEFT,
    Action.MOVE_RIGHT: Player.Direction.RIGHT,
}


def main():
    g_map = Map.get_map_obj(12, 8)
    player = Player(1, 1)
    t_render = TerminalRenderer()
    t_input = TerminalInput()
    while True:
        t_render.draw(g_map, player)
        if check_win(g_map, player):
            print("*" * 9 + " Game Won  " + "*" * 9)
            break
        user_action = t_input.get_action()
        if user_action == Action.QUIT:
            break
        if user_action == Action.NONE:
            continue
        move(g_map, player, ACTION_TO_DIRECTION[user_action])


if __name__ == "__main__":
    main()
