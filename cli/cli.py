import curses
from curses import wrapper


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_RED)

    stdscr.clear()
    stdscr.addstr(10, 20, "Hello World", curses.A_STANDOUT)
    stdscr.addstr(3, 30, "Hello World")
    stdscr.refresh()
    stdscr.getch()


wrapper(main)