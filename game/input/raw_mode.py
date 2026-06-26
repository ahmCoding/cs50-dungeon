import termios
import tty


class RawMode:
    """
    The reason for raw mode is to have an immediate response to a pressed key in
    game without the conformation(enter/no buffering). The game can be closed
    with 'q',so we don't need the cbreak (Ctrl+C) as exit option.
    """

    def __init__(self, fd: int):
        self.fd = fd
        self.old_tty_state = []

    def __enter__(self):
        """
        :return : we return the self object , even though there is no function to
        use with ist.
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
