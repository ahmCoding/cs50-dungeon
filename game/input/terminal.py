from input.action import Action
from input.base import InputSource


class TerminalInput(InputSource):
    STR_TO_ACTION = {
        "w": Action.MOVE_UP,
        "s": Action.MOVE_DOWN,
        "d": Action.MOVE_RIGHT,
        "a": Action.MOVE_LEFT,
        "q": Action.QUIT,
    }

    def get_action(self) -> Action:
        print("w: up , s: down , a: left, d: right, :q for quit")
        user_i = input("Action: ").lower()
        try:
            action = self.STR_TO_ACTION[user_i]
        except KeyError:
            return Action.NONE
        return action
