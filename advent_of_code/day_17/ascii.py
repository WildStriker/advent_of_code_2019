"""ascii intcode logic"""
from typing import DefaultDict, Set, Tuple

from shared.opcodes import process

POUND = ord("#")
NEW_LINE = ord("\n")

BOT_UP = ord("^")
BOT_DOWN = ord("v")
BOT_LEFT = ord("<")
BOT_RIGHT = ord(">")

BOT_CODE = {BOT_UP, BOT_DOWN, BOT_LEFT, BOT_RIGHT}

FUNCTIONS = {"A", "B", "C"}


def is_intersection(position: tuple, scaffold: Set[tuple]) -> bool:
    """determines if a given position is an intersection

    Arguments:
        position {tuple} -- position being checked
        scaffold {Set[tuple]} -- all scaffold locations

    Returns:
        bool -- True if an intersecting piece
    """
    above = (position[0] - 1, position[1])
    if above not in scaffold:
        return False

    below = (position[0] + 1, position[1])
    if below not in scaffold:
        return False

    left = (position[0], position[1] - 1)
    if left not in scaffold:
        return False

    right = (position[0], position[1] + 1)
    if right not in scaffold:
        return False

    return True


def get_intersections(scaffold: Set[tuple]) -> Set[tuple]:
    """returns all intersections

    Arguments:
        scaffold {Set[tuple]} -- all scaffold pieces

    Returns:
        Set[tuple] -- only intersections
    """
    intersections = set()
    for position in scaffold:
        if is_intersection(position, scaffold):
            intersections.add(position)
    return intersections


def alignment_parameter(codes: DefaultDict[int, int]) -> int:
    """calculate the alightment parameters

    Arguments:
        codes {DefaultDict[int, int]} -- intcode machine instructions

    Returns:
        int -- calculated value
    """
    scaffold = set()
    top = 0
    left = 0
    for code in process(codes):
        if code == POUND:
            position = (top, left)
            scaffold.add(position)

        if code == NEW_LINE:
            top += 1
            left = 0
        else:
            left += 1

    total = 0
    for position in get_intersections(scaffold):
        top, left = position
        total += top * left

    return total


def visit_all(codes: DefaultDict[int, int]) -> int:
    """visit all locations and gather dust

    Arguments:
        codes {DefaultDict[int, int]} -- intcode machine instructions

    Returns:
        int -- total dust collected
    """
    # init values
    bot_position = None
    bot_facing = None
    scaffold = set()
    visited = set()
    top = 0
    left = 0
    line = []
    for code in process(codes.copy()):
        if code == POUND:
            position = (top, left)
            scaffold.add(position)
        elif code in BOT_CODE:
            bot_position = (top, left)
            scaffold.add(bot_position)
            visited.add(bot_position)
            bot_facing = code

        if code == NEW_LINE:
            top += 1
            left = 0
            print(''.join(line))
            line = []
        else:
            left += 1
            line.append(chr(code))

    # get direcions, it appears output does not have intersections at "corners"
    # so logic should be "turn" then move forward until end of straight away
    # then find the next "turn" and repeat until the end
    directions = []
    bot_facing, direction = bot_turn(bot_facing, bot_position, scaffold)
    while bot_facing:
        # updates visited scaffolds
        bot_position, moved = bot_move(bot_facing,
                                       bot_position,
                                       scaffold,
                                       visited)
        directions.append(f"{direction} {moved}")
        bot_facing, direction = bot_turn(bot_facing,
                                         bot_position,
                                         scaffold)

    # check that all scaffolds have been visited
    assert scaffold == visited, "Not all positions have been visited"

    # once we determine the full path, we need to compress this into shorter instructions
    main, func_a, func_b, func_c = compress_directions(directions)

    def input_gen(actions):
        for action in ",".join(actions):
            yield ord(action)
        yield NEW_LINE

    main = input_gen(main)

    func_a = input_gen(map(lambda value: value.replace(" ", ","), func_a))
    func_b = input_gen(map(lambda value: value.replace(" ", ","), func_b))
    func_c = input_gen(map(lambda value: value.replace(" ", ","), func_c))

    def display_prompt():
        yield ord("n")
        yield NEW_LINE
    display_prompt = display_prompt()

    def direction_input():
        for value in main:
            return value

        for value in func_a:
            return value

        for value in func_b:
            return value

        for value in func_c:
            return value

        for value in display_prompt:
            return value

    # wake bot up
    codes[0] = 2

    bot_directions = process(codes, direction_input)

    output = 0
    for output in bot_directions:
        pass

    return output


def bot_turn(bot_facing: int, bot_position: tuple, scaffold: Set[tuple]) -> Tuple[int, str]:
    """turn the bot right or left, this is only done on corners so should only
    have one choice

    Arguments:
        bot_facing {int} -- the current bot facing direction
        bot_position {tuple} -- current position
        scaffold {Set[tuple]} -- scaffold locations

    Returns:
        Tuple[int, str] -- new bot_facing location, and direction (turned)
    """
    if bot_facing == BOT_UP:
        # check right
        position = (bot_position[0], bot_position[1] + 1)
        if position in scaffold:
            return BOT_RIGHT, "R"

        # check left
        position = (bot_position[0], bot_position[1] - 1)
        if position in scaffold:
            return BOT_LEFT, "L"

        # nothing!
        return None, None

    if bot_facing == BOT_DOWN:
        # check right (left facing)
        position = (bot_position[0], bot_position[1] - 1)
        if position in scaffold:
            return BOT_LEFT, "R"

        # check left (right facing)
        position = (bot_position[0], bot_position[1] + 1)
        if position in scaffold:
            return BOT_RIGHT, "L"

        # nothing!
        return None, None

    if bot_facing == BOT_LEFT:
        # check right (up facing)
        position = (bot_position[0] - 1, bot_position[1])
        if position in scaffold:
            return BOT_UP, "R"

        # check left (down facing)
        position = (bot_position[0] + 1, bot_position[1])
        if position in scaffold:
            return BOT_DOWN, "L"

        # nothing!
        return None, None

    if bot_facing == BOT_RIGHT:
        # check right (down facing)
        position = (bot_position[0] + 1, bot_position[1])
        if position in scaffold:
            return BOT_DOWN, "R"

        # check left (up facing)
        position = (bot_position[0] - 1, bot_position[1])
        if position in scaffold:
            return BOT_UP, "L"

        # nothing!
        return None, None


def bot_move(bot_facing: int,
             bot_position: tuple,
             scaffold: Set[tuple],
             visited: Set[tuple]) -> Tuple[tuple, int]:
    """move bot in the direction it is facing

    Arguments:
        bot_facing {int} -- direction bot is facing
        bot_position {tuple} -- current position
        scaffold {Set[tuple]} -- scaffold locations
        visited {Set[tuple]} -- scaffolds visited (gets updated when moving)

    Returns:
        Tuple[tuple, int] -- new position, and steps moved
    """
    if bot_facing == BOT_UP:
        top = -1
        left = 0

    if bot_facing == BOT_DOWN:
        top = 1
        left = 0

    if bot_facing == BOT_LEFT:
        top = 0
        left = -1

    if bot_facing == BOT_RIGHT:
        top = 0
        left = 1

    position = (bot_position[0] + top, bot_position[1] + left)
    moved = 0
    while position in scaffold:
        bot_position = position
        moved += 1
        visited.add(position)
        position = (bot_position[0] + top, bot_position[1] + left)

    return bot_position, moved


def compress_directions(directions: str) -> Tuple[list, list, list, list]:
    """compress directions to a list of "functions"

    Arguments:
        directions {list} -- full direction list

    Returns:
        Tuple[list, list, list, list] -- compressed list (main), a, b, c related functions
    """
    main = directions

    func_a = find_repeat(main)
    main = compress_repeat(main, func_a, "A")

    func_b = find_repeat(main)
    main = compress_repeat(main, func_b, "B")

    func_c = find_repeat(main)
    main = compress_repeat(main, func_c, "C")
    return main, func_a, func_b, func_c


def find_repeat(directions: list) -> list:
    """find repeats in direction list
    only a max of 4 per function

    Arguments:
        directions {list} -- list of directions

    Returns:
        list -- sliced section of directions that repeats
    """
    max_match = 4

    # skip compressed patterns
    start_index = 0
    for start_index, direction in enumerate(directions):
        if direction not in FUNCTIONS:
            break

    # index for first pattern
    end_index = start_index

    # index for second pattern
    second_index = end_index + 2

    # directions matched
    match_count = 0

    # look until all results exhausted
    while second_index < len(directions):
        # compare and move to next character
        if directions[end_index] == directions[second_index] \
                and directions[end_index] not in FUNCTIONS \
                and directions[second_index] not in FUNCTIONS:
            match_count += 1
            if match_count == max_match:
                break
            if end_index >= second_index - match_count + 1:
                match_count -= 1
                break
            else:
                end_index += 1
        else:
            # found a match
            if match_count > 1:
                end_index -= 1
                break
            # no matching pattern restart check
            else:
                end_index = start_index
                match_count = 0

        second_index += 1

    return directions[start_index: end_index + 1]


def compress_repeat(directions: list, pattern: list, letter: str) -> list:
    """replace pattern found in directions with a given letter

    Arguments:
        directions {list} -- list of directions
        pattern {list} -- repeated pattern
        letter {str} -- substitute

    Returns:
        list -- list with repeated value compressed
    """
    directions = ','.join(directions)
    pattern = ','.join(pattern)

    directions = directions.replace(pattern, letter)

    return directions.split(",")
