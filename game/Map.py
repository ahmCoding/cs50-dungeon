import random

from game.Player import Player


class Map:
    def __init__(self,h:int=5,w:int=5):
        self._height=h
        self._width= w
        self._map_chars={'wall':'#','field':'.','stairs':'>','player':'@'}
        self._map=[]

    def _create_map(self):
        r_x=random.randint(1,self._width-2)
        r_y=random.randint(1,self._height-2)

        tmp_map=[[self._map_chars['wall'] for w in range(self._width)] for h in range(self._height)]
        #only writhe somewhere in the middle of field
        for h in range(1,self._height-1):
            for w in range(1,self._width-1):
                if h==r_y and w==r_x:
                    tmp_map[h][w]=self._map_chars['stairs']
                else:
                    tmp_map[h][w]=self._map_chars['field']
        self._map=tmp_map

    @classmethod
    def get_map(cls,h:int=5,w:int=5):
        tmp_obj=cls(h,w)
        tmp_obj._create_map()
        return tmp_obj

    @staticmethod
    def _map_to_string(game_map:list)->str:
        tmp_map = ""
        for row in game_map:
            tmp_map += "".join(row)
            tmp_map += "\n"
        return tmp_map

    def __str__(self):
        return self._map_to_string(self._map)

    def is_movable(self,x,y):
        return self._map[y][x]!=self._map_chars['wall']

    def render(self,player:Player) -> str:
        rendered_map=[[self._map[h][w] for w in range(self._width)]for h in range(self._height)] # deep copy
        for h in range(self._height):
            for w in range(self._width):
                if player.x == w and player.y == h:
                    if self.is_movable(w,h):
                        rendered_map[h][w]=self._map_chars['player']
        return self._map_to_string(rendered_map)




def main():
    map_obj=Map.get_map(8,12)
    p1=Player(1,1)

    print(map_obj.render(p1),end="")

if __name__=="__main__":
    main()


