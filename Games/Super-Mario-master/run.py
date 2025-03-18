import curses
from config import Engine

def main(win):
    # Optionally initialize curses color pairs here
    engine = Engine()
    engine.win = win
    engine.run()
def play():
    curses.wrapper(main)