from enum import Enum

class Player:
    class Direction(Enum):
        UP=(-1,0)
        DOWN=(1,0)
        LEFT=(0,-1)
        RIGHT=(0,1)

    def __init__(self,x:int=0,y:int=0):
        self.x=x
        self.y=y

    def move(self,direction:Direction):
        dy,dx=direction.value
        self.x+=dx
        self.y+=dy

