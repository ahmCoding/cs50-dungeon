from game.core.map import Map
from game.core.player import Player
from game.input.action import Action
from game.input.base import InputSource
from game.input.terminal import TerminalInput
from game.render.base import Renderer
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


def play(
    g_map: Map, player: Player, in_source: InputSource, renderer: Renderer
) -> None:
    while True:
        renderer.draw(g_map, player)
        if check_win(g_map, player):
            print("*" * 9 + " Game Won  " + "*" * 9)
            break
        user_action = in_source.get_action()
        if user_action == Action.QUIT:
            break
        if user_action == Action.NONE:
            continue
        move(g_map, player, ACTION_TO_DIRECTION[user_action])


def main():
    g_map = Map.get_map_obj(12, 8)
    player = Player(1, 1)
    t_render = TerminalRenderer()
    t_input = TerminalInput()
    print("w: up , s: down , a: left, d: right, q for quit")
    play(g_map, player, t_input, t_render)


if __name__ == "__main__":
    main()
