from game.input.action import Action
from game.input.terminal import TerminalInput


class CanonicalTerminal(TerminalInput):
    def get_action(self) -> Action:
        user_i = input("Action: ").lower()
        return self.map_str_to_action(user_i)
