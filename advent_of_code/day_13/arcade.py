"""game logic module"""
import collections
from typing import DefaultDict, Dict, Tuple

import click

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


def draw_board(board: Dict[tuple, int],
               score: int,
               max_height: int,
               max_width: int) -> Tuple[tuple, tuple]:
    """draw game board, returns current paddle and ball positions

    Arguments:
        board {Dict[tuple, int]} -- board state
        score {int} -- current score
        max_height {int} -- max tile height
        max_width {int} -- max tile width

    Returns:
        Tuple[tuple, tuple] -- paddle, ball positions
    """
    for top in range(max_height + 1):
        line = []
        for left in range(max_width + 1):
            position = (top, left)
            tile = board[position]
            if tile == BALL:
                ball = position
            elif tile == PADDLE:
                paddle = position
            line.append(TILE_OUTPUT[tile])
        print(''.join(line))
    print(f"Score: {score}")
    return paddle, ball


def play(codes: DefaultDict[int, int], is_human: bool):
    """play the game!

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions
        is_human {bool} -- read in user input if true (fun, but very...slow...)
    """
    board = {}

    steps = 0
    max_height = 0
    max_width = 0

    # for user inputs
    def draw_input():
        draw_board(board, score, max_height, max_width)
        return click.prompt("joystick position", type=click.IntRange(-1, 1))

    # for automatic inputs
    def draw_ai():
        paddle, ball = draw_board(board, score, max_height, max_width)

        if paddle[1] == ball[1]:
            return 0

        if paddle[1] > ball[1]:
            return -1

        return 1

    if is_human:
        game = process(codes, draw_input)
    else:
        game = process(codes, draw_ai)

    for left in game:
        steps += 1
        top = next(game)
        position = (top, left)

        max_width = max(max_width, left)
        max_height = max(max_height, top)

        if position == (0, -1):
            score = next(game)
        else:
            tile = next(game)
            board[(top, left)] = tile

    print("Game Complete!")
    draw_board(board, score, max_height, max_width)
