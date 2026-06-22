import random

class Map:
    def __init__(self,w:int=5,h:int=5):
        """
        :param w: width of the map /x
        :param h: height of the map /y
        """
        self._height=h
        self._width= w
        self._map_chars={'wall':'#','field':'.','stairs':'>'}
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
    def get_map_obj(cls,w:int=5,h:int=5):
        tmp_obj=cls(w,h)
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
        if 0 <= x < self._width and 0 <= y < self._height:
            return self.get_tile(x,y)!=self._map_chars['wall']
        return False

    def get_game_map(self)->list[list[str]]:
        return [[self._map[h][w] for w in range(self._width)] for h in range(self._height)]

    def draw_as_a_map(self,l_map:list[list[str]])->str:
        return self._map_to_string(l_map)

    def get_tile(self,x,y):
        return self._map[y][x]

    def get_win_tile(self)-> str:
        return self._map_chars['stairs']