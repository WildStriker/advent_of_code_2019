"""key path finding module"""
import queue
from typing import List, TextIO


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


def get_shortest(start: tuple, path: dict, keys: set, doors: set) -> int:
    """find the shortest path to all keys
    doors are in a lock state until corresponding key is collected

    Arguments:
        start {tuple} -- starting positition
        path {dict} -- non-wall path
        keys {set} -- keys (lower case letters)
        doors {set} -- doors (upper case letter)

    Returns:
        int -- total steps
    """
    frontier = queue.PriorityQueue()

    start_state = (start, frozenset())
    frontier.put((0, start_state))

    came_from = {
        start_state: None
    }
    cost_so_far = {
        start_state: 0
    }

    weight = 1
    while not frontier.empty():
        _, current = frontier.get()

        current_position = current[0]
        current_keys = current[1]
        if current_keys == keys:
            break

        for neighbor in get_neighbors(*current_position):
            if neighbor not in path:
                continue

            if path[neighbor] in doors and path[neighbor].lower() not in current_keys:
                continue

            if path[neighbor] in keys:
                neighbor_keys = set(current_keys)
                neighbor_keys.add(path[neighbor])
                neighbor_keys = frozenset(neighbor_keys)
            else:
                neighbor_keys = current_keys

            neighbor_state = (neighbor, neighbor_keys)
            new_cost = cost_so_far[current] + weight
            if neighbor_state not in cost_so_far or new_cost < cost_so_far[neighbor_state]:
                cost_so_far[neighbor_state] = new_cost
                priority = new_cost + len(keys) - len(neighbor_keys)
                frontier.put((priority, neighbor_state))
                came_from[neighbor_state] = current

    for key in came_from:
        if key[1] == keys:
            return cost_so_far[key]


def read_input(file_input: TextIO) -> tuple:
    """get starting position, "walkable" path
    keys and doors from input file

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        tuple -- start, path, keys doors
    """
    start = None
    keys = set()
    doors = set()
    path = {}
    for y_pos, line in enumerate(file_input):
        for x_pos, tile in enumerate(line.strip()):
            if tile == "#":
                continue

            position = (y_pos, x_pos)

            path[position] = tile

            code = ord(tile)
            if tile == "@":
                start = position
            elif code >= 65 and code <= 90:
                doors.add(tile)
            elif code >= 97 and code <= 122:
                keys.add(tile)
    return start, path, keys, doors


def read_quadrants(file_input: TextIO) -> tuple:
    """read text input into 4 quadrants

    The robots do not need to backtrack in its own quadrant when there
    is a locked door it can not collect a key for, instead it waits until
    another bot collects a key.

    We can assume all keys from other quadrants are already available and remove
    unwanted doors

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        tuple -- quadrants 1, 2, 3, 4 (see read input)
    """
    start, path, keys, doors = read_input(file_input)

    nw_start = (start[0]-1, start[1]-1)
    nw_path = {}
    nw_keys = set()
    nw_doors = set()

    ne_start = (start[0] - 1, start[1]+1)
    ne_path = {}
    ne_keys = set()
    ne_doors = set()

    se_start = (start[0] + 1, start[1]+1)
    se_path = {}
    se_keys = set()
    se_doors = set()

    sw_start = (start[0] + 1, start[1]-1)
    sw_path = {}
    sw_keys = set()
    sw_doors = set()

    for position in path:
        tile = path[position]
        # north quadrant
        if position[0] < start[0]:
            if position[1] > start[1]:
                ne_path[position] = tile
                if tile in keys:
                    ne_keys.add(tile)
                if tile in doors:
                    ne_doors.add(tile)
            else:
                nw_path[position] = tile
                if tile in keys:
                    nw_keys.add(tile)
                if tile in doors:
                    nw_doors.add(tile)
        # south quadrant
        else:
            if position[1] > start[1]:
                se_path[position] = tile
                if tile in keys:
                    se_keys.add(tile)
                if tile in doors:
                    se_doors.add(tile)
            else:
                sw_path[position] = tile
                if tile in keys:
                    sw_keys.add(tile)
                if tile in doors:
                    sw_doors.add(tile)

    # open doors if keys are in other quadrants
    nw_doors = ne_doors - set(map(str.upper, ne_keys | se_keys | sw_keys))
    ne_doors = ne_doors - set(map(str.upper, nw_keys | se_keys | sw_keys))
    se_doors = ne_doors - set(map(str.upper, nw_keys | ne_keys | sw_keys))
    sw_doors = ne_doors - set(map(str.upper, nw_keys | ne_keys | se_keys))

    quad_1 = (nw_start, nw_path, nw_keys, nw_doors)
    quad_2 = (ne_start, ne_path, ne_keys, ne_doors)
    quad_3 = (se_start, se_path, se_keys, se_doors)
    quad_4 = (sw_start, sw_path, sw_keys, sw_doors)
    return quad_1, quad_2, quad_3, quad_4
