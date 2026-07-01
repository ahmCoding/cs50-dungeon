from game.core.level import Level


class Dungeon:
    """
    this class represents a dungeon which is a container for levels
    """

    def __init__(self, levels: list[Level]):
        self._levels = levels
        self._idx_current_level = 0

    def get_current_level(self) -> Level:
        return self._levels[self._idx_current_level]

    def next_level(self) -> None:
        if not self.is_last_level():
            self._idx_current_level += 1

    def is_last_level(self) -> bool:
        """
        :return: True if the current level is the last level
        """
        return self._idx_current_level == len(self._levels) - 1
