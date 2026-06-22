from Player import Player
from Map import Map

def render(g_map:Map,player:Player)->str:
    rendered_map = g_map.get_game_map()
    rendered_map[player.y][player.x] = player.char
    return g_map.draw_as_a_map(rendered_map)

def move(g_map:Map,player:Player,key:str):
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
    new_x,new_y=player.next_position(direction)
    if g_map.is_movable(new_x,new_y):
        player.move(direction)