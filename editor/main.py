import argparse
import curses
from typing import Optional
from typing import Sequence

from .buf import Buffer
from .window import Window


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args(argv)

    return curses.wrapper(c_main, args.filename)


def c_main(stdscr: "curses._CursesWindow", filename: str) -> int:
    with open(filename) as f:
        lines = f.read().split("\n")

    buf = Buffer(lines)
    window = Window(buf, curses.COLS, curses.LINES)

    while True:
        # Update screen
        for y, line in enumerate(window.lines):
            stdscr.addstr(y, 0, line)
        stdscr.move(window.cy, window.cx)

        # Handle keypresses
        c = stdscr.getkey()
        if c == "q":
            break
        elif c == "k":
            buf.up()
        elif c == "j":
            buf.down()
        elif c == "h":
            buf.left()
        elif c == "l":
            buf.right()
        elif c == "0":
            buf.home()
        elif c == "$":
            buf.end()

    return 0
