class Weapon:
    def __init__(self, damage: int = 1):
        """
        :param damage: the damage which is caused by the weapon
        """
        self._damage = damage

    def get_damage(self) -> int:
        """function to return the damage points of the weapon"""
        return self._damage
