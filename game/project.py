from Player import Player
from Map import Map

def render(g_map:Map,player:Player)->str:
    rendered_map = g_map.get_game_map()
    rendered_map[player.y][player.x] = player.char
    return g_map.draw_as_a_map(rendered_map)

def move(g_map:Map,player:Player,key:str):
    match key:
        case "w":
            player.move(Player.Direction.UP)
            if not g_map.is_movable(player.y,player.x):
                player.move(Player.Direction.DOWN)
        case "s":
            player.move(Player.Direction.DOWN)
            if not g_map.is_movable(player.y, player.x):
                player.move(Player.Direction.UP)
        case "a":
            player.move(Player.Direction.LEFT)
            if not g_map.is_movable(player.y, player.x):
                player.move(Player.Direction.RIGHT)

        case "d":
            player.move(Player.Direction.RIGHT)
            if not g_map.is_movable(player.y, player.x):
                player.move(Player.Direction.LEFT)
