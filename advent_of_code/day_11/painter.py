"""amplify logic module"""
from typing import Dict, List

from shared.opcodes import process

BLACK = 0
WHITE = 1

PAINTED_OUTPUT = {
    BLACK: ".",
    WHITE: "#"
}

TURN_LEFT = 0
TURN_RIGHT = 1

UP = 0
RIGHT = 0.25
DOWN = 0.5
LEFT = 0.75


def paint(codes: List[int], painted: Dict[tuple, int] = None) -> Dict[tuple, int]:
    """read paint instructions from intcode computer with provided inputs

    Arguments:
        codes {List[int]} -- intcode inputs, this will output the robots paint instructions

    Keyword Arguments:
        painted {Dict[tuple, int]} -- initial haul paint (default: {None})
                                      coords not given are assumed painted

    Returns:
        Dict[tuple, int] -- haul paint
    """
    # init painted dictionary
    if painted is None:
        painted = {}

    direction = 0

    # start intcode machine
    result = process(codes)

    position = (0, 0)
    for _ in result:
        _ok = result.send(painted.get(position, BLACK))

        color = next(result)
        painted[position] = color

        turn = next(result)

        # turn
        if turn == TURN_RIGHT:
            direction += 0.25
            if direction == 1:
                direction = 0
        elif turn == TURN_LEFT:
            direction -= 0.25
            if direction == -0.25:
                direction = 0.75
        else:
            ValueError("Invalid turn: {turn}")

        # move forward based on direction
        if direction == UP:
            position = (position[0] - 1, position[1])
        elif direction == RIGHT:
            position = (position[0], position[1] + 1)
        elif direction == DOWN:
            position = (position[0] + 1, position[1])
        elif direction == LEFT:
            position = (position[0], position[1] - 1)
    return painted


def render_painted(codes: List[int], painted: Dict[tuple, int]):
    """print painted haul to screen

    Arguments:
        codes {List[int]} -- intcode instructions
        painted {Dict[tuple, int]} -- starting haul paint
    """
    painted = paint(codes, painted)

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    # find range we want to render to screen
    for coord in painted:
        if coord[0] < min_y:
            min_y = coord[0]
        if coord[0] > max_y:
            max_y = coord[0]

        if coord[1] < min_x:
            min_x = coord[1]
        if coord[1] > max_x:
            max_x = coord[1]

    # render painted haul
    for y_pos in range(min_y, max_y + 1):
        output = []
        for x_pos in range(min_x, max_x + 1):
            panel = PAINTED_OUTPUT[painted.get((y_pos, x_pos), BLACK)]
            output.append(panel)
        print(''.join(output))


def count_painted(codes: List[int]) -> int:
    """count all panels the robot has painted

    Arguments:
        codes {List[int]} -- intcode instructions

    Returns:
        int -- painted panel count
    """
    painted = paint(codes)
    return len(painted)
