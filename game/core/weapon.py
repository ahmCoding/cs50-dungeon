class Weapon:
    def __init__(self, damage: int = 1):
        self._damage = damage

    def get_damage(self):
        return self._damage
