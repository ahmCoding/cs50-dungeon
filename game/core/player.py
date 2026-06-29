from game.core.character import Character


class Player(Character):
    """
    this class represents a player in the game
    """

    def next_position(self, direction: Character.Direction) -> tuple[int, int]:
        dx, dy = direction.value
        return self.x + dx, self.y + dy
