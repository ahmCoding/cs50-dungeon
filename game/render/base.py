from abc import ABC, abstractmethod

from game.core.character import Character
from game.core.map import Map


class Renderer(ABC):
    @abstractmethod
    def draw(self, g_map: Map, characters: list[Character]) -> None:
        pass
