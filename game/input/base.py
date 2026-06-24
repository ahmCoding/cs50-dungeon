from abc import ABC, abstractmethod

from game.input.action import Action


class InputSource(ABC):
    @abstractmethod
    def get_action(self) -> Action:
        pass
