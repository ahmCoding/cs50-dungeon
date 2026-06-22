class Player:
    def __init__(self,x:int=0,y:int=0):
       self.x=x
       self.y=y

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,x:int):
        self._x=x

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,y:int):
        self._y=y


    def move(self,x,y):
        self.x=x
        self.y=y

    @classmethod
    def get_player(cls,x:int,y:int):
        player=cls(x,y)
        return player