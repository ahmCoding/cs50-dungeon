import sys

from game.core.dungeon import Dungeon
from game.core.enemy import Enemy
from game.core.map import Map
from game.core.player import Player
from game.input.action import Action
from game.input.base import InputSource
from game.input.raw_terminal import RawTerminal
from game.render.base import Renderer
from game.render.terminal import TerminalRenderer


def move(g_map: Map, player: Player, p_direction: Player.Direction):
    """function that moves the character according to the given direction
    on the given map"""
    new_x, new_y = player.next_position(p_direction)
    if g_map.is_movable(new_x, new_y):
        player.move(p_direction)


def is_won(g_dungeon: Dungeon, player: Player) -> bool:
    if g_dungeon.is_last_map():
        return check_stairs(g_dungeon.get_current_map(), player)
    return False


def check_stairs(g_map: Map, player: Player) -> bool:
    """
    :return: True if the player is on a stairs tile
    """
    return g_map.get_tile(player.x, player.y) == g_map.get_stairs_tile()


# to map ACTION to Player.Direction
ACTION_TO_DIRECTION = {
    Action.MOVE_UP: Player.Direction.UP,
    Action.MOVE_DOWN: Player.Direction.DOWN,
    Action.MOVE_LEFT: Player.Direction.LEFT,
    Action.MOVE_RIGHT: Player.Direction.RIGHT,
}


def descend(g_dungeon: Dungeon, player: Player) -> None:
    """
    descend to the deeper map and set the player on the start position of the map
    """
    g_dungeon.next_map()
    player.set_position(*g_dungeon.get_current_map().get_start_position())


def play(
    g_dungeon: Dungeon,
    player: Player,
    enemy: Enemy,
    in_source: InputSource,
    renderer: Renderer,
) -> None:
    while True:
        renderer.draw(g_dungeon.get_current_map(), [player, enemy])

        # the player has won the game , if he is on the last
        # map and on a stairs tile
        if is_won(g_dungeon, player):
            print("*" * 9 + " Game Won  " + "*" * 9)
            break
        user_action = in_source.get_action()
        if user_action == Action.QUIT:
            break
        if user_action == Action.NONE:
            continue
        move(g_dungeon.get_current_map(), player, ACTION_TO_DIRECTION[user_action])
        # next map
        if check_stairs(g_dungeon.get_current_map(), player):
            if not g_dungeon.is_last_map():
                descend(g_dungeon, player)
        enemy.my_turn_to_move(g_dungeon.get_current_map())


def main():
    fd = sys.stdin.fileno()  # raw input mode
    raw_terminal_input = RawTerminal(fd)

    g_map1 = Map.get_map_obj(12, 8)
    g_map2 = Map.get_map_obj(12, 8)
    g_dungeon = Dungeon([g_map1, g_map2])
    player = Player(1, 1)
    enemy = Enemy(1, 3)  # only a random chosen pos for enemy
    t_render = TerminalRenderer()
    # t_input = TerminalInput()
    print("w: up , s: down , a: left, d: right, q for quit")
    play(g_dungeon, player, enemy, raw_terminal_input, t_render)


if __name__ == "__main__":
    main()
