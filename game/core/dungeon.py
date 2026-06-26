from game.core.map import Map


class Dungeon:
    """
    this class represents a dungeon which is a container for maps
    """

    def __init__(self, maps: list[Map]):
        self.maps = maps
        self._idx_current_map = 0

    def get_current_map(self) -> Map:
        return self.maps[self._idx_current_map]

    def next_map(self) -> Map:
        self._idx_current_map += 1
        return self.get_current_map()

    def is_last_map(self) -> bool:
        """
        :return: True if the current map is the last map
        """
        return self._idx_current_map == len(self.maps) - 1
