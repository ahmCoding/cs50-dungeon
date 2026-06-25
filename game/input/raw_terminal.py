import sys

from game.input.action import Action
from game.input.raw_mode import RawMode
from game.input.terminal import TerminalInput


class RawTerminal(TerminalInput):
    def __init__(self, fd: int):
        self.raw_context_manager = RawMode(fd)

    def get_action(self) -> Action:
        with self.raw_context_manager:
            char = sys.stdin.read(1)
        return self.map_str_to_action(char)
