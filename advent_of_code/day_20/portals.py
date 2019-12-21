"""portal\\recursive maze module"""
import queue
from typing import List, TextIO

from shared.distance import manhattan_distance


def get_neighbors(y_pos: int, x_pos: int) -> List[tuple]:
    """get neighboring coordinators to a given position

    Arguments:
        y_pos {int} -- given y position
        x_pos {int} -- given x position

    Returns:
        List[tuple] -- 4 neighboring coordinates
    """
    neighbors = []
    # up
    up_coord = (y_pos-1, x_pos)
    neighbors.append(up_coord)

    # left
    left_coord = (y_pos, x_pos - 1)
    neighbors.append(left_coord)

    # right
    right_coord = (y_pos, x_pos + 1)
    neighbors.append(right_coord)

    # down
    down_coord = (y_pos+1, x_pos)
    neighbors.append(down_coord)

    return neighbors


def get_shortest(start: tuple,
                 goal: tuple,
                 path: dict,
                 outter_portals: dict,
                 inner_portals: dict,
                 is_level_aware: bool = False) -> int:
    """find the shortest path goal


    Arguments:
        start {tuple} -- starting positition
        goal {tuple} -- target position
        path {dict} -- non-wall path
        outter_portals {dict} -- portal links on the outside
        inner_portals {dict} -- portal links on the inside
        is_level_aware {dict} -- portals link

    Keyword Arguments:
        is_level_aware {bool} -- portals behave "recursively" (default: {False})

    Returns:
        int -- total steps
    """
    frontier = queue.PriorityQueue()

    level = 0
    start_state = (start, level)
    frontier.put((0, start_state))

    came_from = {
        start_state: None
    }
    cost_so_far = {
        start_state: 0
    }

    while not frontier.empty():
        _, current = frontier.get()

        current_position = current[0]
        current_level = current[1]
        if current == (goal, 0):
            break

        for neighbor in get_neighbors(*current_position):
            weight = 1
            neighbor_level = current_level
            if neighbor not in path:
                continue

            # portal, telport neighbor position!
            if neighbor in outter_portals:
                neighbor = outter_portals[neighbor]
                weight += 1
                if is_level_aware:
                    if current_level == 0:
                        continue
                    else:
                        neighbor_level -= 1
            elif neighbor in inner_portals:
                neighbor = inner_portals[neighbor]
                weight += 1
                if is_level_aware:
                    neighbor_level += 1

            neighbor_state = (neighbor, neighbor_level)
            new_cost = cost_so_far[current] + weight
            if neighbor_state not in cost_so_far or new_cost < cost_so_far[neighbor_state]:
                cost_so_far[neighbor_state] = new_cost
                priority = new_cost + neighbor_level + \
                    manhattan_distance(neighbor, goal)
                frontier.put((priority, neighbor_state))
                came_from[neighbor_state] = current_position

    if (goal, 0) in cost_so_far:
        return cost_so_far[(goal, 0)]


def read_input(file_input: TextIO) -> tuple:
    """read map to get initial state

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        tuple -- start, goal, path, portals
    """

    all_tiles = {}
    start = None
    goal = None
    path = {}

    # mapped "XX" letter to first portal position
    first_portal = {}

    # link portal positions one to one
    is_outter = None
    inner_portals = {}
    outter_portals = {}

    path = {}
    max_x = 0
    max_y = 0

    for y_pos, line in enumerate(file_input):
        for x_pos, tile in enumerate(line.replace("\n", "")):
            position = (y_pos, x_pos)
            all_tiles[position] = tile
            max_x = max(max_x, x_pos)
        max_y = max(max_y, y_pos)

    for y_pos in range(max_y + 1):
        for x_pos in range(max_x + 1):
            position = (y_pos, x_pos)

            tile = all_tiles[position]
            if tile in {"#", " "}:
                continue

            path[position] = tile

            code = ord(tile)
            # check if letter is read beside it
            # (left or above)
            if code >= 65 and code <= 90:
                # flag for outter \ inner portals
                if x_pos < 2 or y_pos < 2 or x_pos > max_x - 2 or y_pos > max_y - 2:
                    is_outter = True
                else:
                    is_outter = False

                letters = tile

                # left
                position_left = (y_pos, x_pos - 1)
                if position_left in path:
                    code = path[position_left]
                    code = ord(code)
                    if code >= 65 and code <= 90:
                        letters = path[position_left] + letters

                        letter_location = (y_pos, x_pos - 2)
                        if letter_location not in path:
                            # location is to the right
                            letter_location = (y_pos, x_pos + 1)

                        # check if this is a starting or goal location first
                        if letters == "AA":
                            start = letter_location
                        elif letters == "ZZ":
                            goal = letter_location
                        elif letters in first_portal:
                            if is_outter:
                                outter_portals[letter_location] = first_portal[letters]
                                inner_portals[first_portal[letters]
                                              ] = letter_location
                            else:
                                outter_portals[first_portal[letters]
                                               ] = letter_location
                                inner_portals[letter_location] = first_portal[letters]
                        else:
                            first_portal[letters] = letter_location

                # above
                position_above = (y_pos - 1, x_pos)
                if position_above in path:
                    code = path[position_above]
                    code = ord(code)
                    if code >= 65 and code <= 90:
                        letters = path[position_above] + letters

                        letter_location = (y_pos - 2, x_pos)
                        if letter_location not in path:
                            # location is below
                            letter_location = (y_pos + 1, x_pos)

                        # check if this is a starting or goal location first
                        if letters == "AA":
                            start = letter_location
                        elif letters == "ZZ":
                            goal = letter_location
                        elif letters in first_portal:
                            if is_outter:
                                outter_portals[letter_location] = first_portal[letters]
                                inner_portals[first_portal[letters]
                                              ] = letter_location
                            else:
                                outter_portals[first_portal[letters]
                                               ] = letter_location
                                inner_portals[letter_location] = first_portal[letters]
                        else:
                            first_portal[letters] = letter_location

    return start, goal, path, outter_portals, inner_portals
