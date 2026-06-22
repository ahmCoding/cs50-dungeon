from enum import Enum

class Player:
    class Direction(Enum):
        """"
        The Enum representing the direction of the player.
        Technically we have the coordination in y,x format
        """
        UP=(-1,0)
        DOWN=(1,0)
        LEFT=(0,-1)
        RIGHT=(0,1)

    def __init__(self,y:int=0,x:int=0,char:str="@"):
        self.x=x
        self.y=y
        self.char=char

    def move(self,direction:Direction):
        dy,dx=direction.value
        self.x+=dx
        self.y+=dy

