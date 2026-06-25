import termios
import tty


class RawMode:
    def __init__(self, fd: int):
        self.fd = fd
        self.old_tty_state = []

    def __enter__(self):
        """
         we are using 'raw' and not 'cbreak',because the user can quit the game with "q"
        and we don't want a complex key-mapping with keys like arrows etc., the priority
        ist the cross-platform ability of the game
        we don't need it as this context manager doesn't offer a
        function beside '__enter__ ' and '__exit__'
        """
        self.old_tty_state = termios.tcgetattr(self.fd)
        tty.setraw(
            self.fd, termios.TCSADRAIN
        )  # transmit all output, but keep the inputted char
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(
            self.fd, termios.TCSADRAIN, self.old_tty_state
        )  # back to original tty-settings
