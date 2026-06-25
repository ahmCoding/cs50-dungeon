import sys
import termios
import tty

from game.input.action import Action
from game.input.terminal import TerminalInput


class RawTerminalInput(TerminalInput):
    def __init__(self, fd):
        self.fd = fd
        self.old_tty_state = []

    def __enter__(self):
        """
         we are using 'raw' and not 'cbreak',because the user can quit the game with "q"
        and we don't want a complex key-mapping with keys like arrows etc., the priority
        ist the cross-platform ability of the game
        """
        self.old_tty_state = termios.tcgetattr(self.fd)
        tty.setraw(
            self.fd, termios.TCSADRAIN
        )  # transmit all output, but keep the inputted char

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(
            self.fd, termios.TCSADRAIN, self.old_tty_state
        )  # back to original tty-settings

    def get_action(self) -> Action:
        with self:
            char = sys.stdin.read(1)
            return self.map_str_to_action(char)
