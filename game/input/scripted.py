from game.input.action import Action
from game.input.base import InputSource


class ScriptedTerminal(InputSource):
    """
    this class is used to get input from the scripted terminal,
    the goal is to test different game loops like an integration test
    """

    def __init__(self, actions: list[Action]):
        self.actions = iter(actions)
        self.current_action = None

    def get_action(self) -> Action:
        self.current_action = next(self.actions)
        return self.current_action
