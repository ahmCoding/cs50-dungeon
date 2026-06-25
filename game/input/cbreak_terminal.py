from game.input.action import Action
from game.input.terminal import TerminalInput


class CbreakTerminal(TerminalInput):
    STR_TO_ACTION = {
        "w": Action.MOVE_UP,
        "s": Action.MOVE_DOWN,
        "d": Action.MOVE_RIGHT,
        "a": Action.MOVE_LEFT,
        "q": Action.QUIT,
    }

    def get_action(self) -> Action:
        user_i = input("Action: ").lower()
        return self.map_str_to_action(user_i)
