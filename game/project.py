from Player import Player
from Map import Map

def render(g_map:Map,player:Player)->str:
    rendered_map = g_map.get_game_map()
    rendered_map[player.y][player.x] = player.char
    return g_map.draw_as_a_map(rendered_map)

def move(g_map:Map,player:Player,key:str):
    match key:
        case "w":
            if g_map.is_movable(player.y-1,player.x):
                player.move(Player.Direction.UP)
        case "s":
            if g_map.is_movable(player.y+1, player.x):
                player.move(Player.Direction.DOWN)
        case "a":
            if g_map.is_movable(player.y, player.x-1):
                player.move(Player.Direction.LEFT)

        case "d":
            if g_map.is_movable(player.y, player.x+1):
                player.move(Player.Direction.RIGHT)
