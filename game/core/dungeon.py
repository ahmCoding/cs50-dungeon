from game.core.map import Map


class Dungeon:
    """
    this class represents a dungeon which is a container for maps
    """

    def __init__(self, maps: list[Map]):
        self._maps = maps
        self._idx_current_map = 0

    def get_current_map(self) -> Map:
        return self._maps[self._idx_current_map]

    def next_map(self) -> None:
        if not self.is_last_map():
            self._idx_current_map += 1

    def is_last_map(self) -> bool:
        """
        :return: True if the current map is the last map
        """
        return self._idx_current_map == len(self._maps) - 1
