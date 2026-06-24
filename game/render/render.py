from abc import ABC, abstractmethod

from game.core.map import Map
from game.core.player import Player


class Render(ABC):
    @abstractmethod
    def draw(self, g_map: Map, player: Player) -> None:
        pass
