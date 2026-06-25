from game.input.action import Action
from game.input.base import InputSource


class ScriptedInput(InputSource):
    """
    this class is used to get input from a script / list,
    the goal is to test different game loops like an integration test
    """

    def __init__(self, actions: list[Action]):
        self.actions = iter(actions)

    def get_action(self) -> Action:
        return next(self.actions)
