from abc import ABC, abstractmethod

from game.input.action import Action


class InputSource(ABC):
    """
    this class represents the input source for the game
    """

    @abstractmethod
    def get_action(self) -> Action:
        pass
