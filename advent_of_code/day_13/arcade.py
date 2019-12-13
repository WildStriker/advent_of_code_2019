"""game logic module"""
import collections
import curses
from typing import DefaultDict

from shared.opcodes import process

EMPTY = 0  # an empty tile. No game object appears in this tile.
WALL = 1  # a wall tile. Walls are indestructible barriers.
BLOCK = 2  # a block tile. Blocks can be broken by the ball.
PADDLE = 3  # a horizontal paddle tile. The paddle is indestructible.
BALL = 4  # a ball tile. The ball moves diagonally and bounces off objects.

TILE_OUTPUT = {
    EMPTY: " ",
    WALL: "X",
    BLOCK: "~",
    PADDLE: "_",
    BALL: "*"
}


def count_block(codes: DefaultDict[int, int]) -> int:
    """count all BLOCK tiles

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions

    Returns:
        int -- total block tiles
    """
    board = {}
    game = process(codes)

    for left in game:
        top = next(game)
        tile = next(game)
        board[(top, left)] = tile

    count = collections.Counter(board.values())
    return count[BLOCK]


def play(codes: DefaultDict[int, int], is_human: bool):
    """play the game!

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions
        is_human {bool} -- read in user input if true (fun, but very...slow...)
    """
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    screen.keypad(True)

    steps = 0
    max_height = 0
    max_width = 0
    paddle = (0, 0)
    ball = (0, 0)

    # for user inputs
    def draw_input():
        screen.refresh()
        key = screen.getch()
        if key == curses.KEY_LEFT:
            return -1
        if key == curses.KEY_RIGHT:
            return 1
        return 0

    # for automatic inputs
    def draw_ai():
        screen.refresh()
        if paddle[1] == ball[1]:
            return 0

        if paddle[1] > ball[1]:
            return -1

        return 1

    if is_human:
        game = process(codes, draw_input)
    else:
        game = process(codes, draw_ai)

    try:
        for left in game:
            steps += 1
            top = next(game)
            position = (top, left)

            max_width = max(max_width, left)
            max_height = max(max_height, top)

            if position == (0, -1):
                score = next(game)
                screen.addstr(max_height + 1, 0, f"Score: {score}")
            else:
                tile = next(game)
                if tile == BALL:
                    ball = position
                elif tile == PADDLE:
                    paddle = position
                screen.addstr(top, left, TILE_OUTPUT[tile])

        message_1 = "Game Complete!"
        message_2 = "Press Any Key to Exit..."
        screen.addstr(max_height // 2, max_width // 2 -
                      len(message_1) // 2, message_1)
        screen.addstr(max_height // 2 + 1, max_width //
                      2 - len(message_2) // 2, message_2)
        screen.refresh()
        screen.getch()
    except curses.error:
        print("Please resize the terminal in order to run the game!")
    finally:
        curses.endwin()
