from game.core.map import Map
from game.core.player import Player
from game.render.base import Renderer


class NullRenderer(Renderer):
    """
    this class is user mainly for test purposes
    """

    def draw(self, g_map: Map, player: Player) -> None:
        pass
