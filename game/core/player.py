from game.core.character import Character
from game.core.weapon import Weapon


class Player(Character):
    """
    this class represents a player in the game
    """

    @classmethod
    def get_player_obj(cls, x: int = 0, y: int = 0, c_weapon: Weapon | None = None):
        """function to create an Enemy object / factory
        :param x: x position of the character / width
        :param y: y position of the character / height
        :param c_weapon: weapon of the character
        """
        if c_weapon is None:
            c_weapon = Weapon()
        return cls(x=x, y=y, weapon=c_weapon)
