"""bugs logic"""
from typing import List, TextIO, Tuple, Union


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


def neighbor_bugs(depth: int,
                  y_pos: int, x_pos:
                  int, bugs: set,
                  inner_depth: tuple,
                  y_count: int,
                  x_count: int) -> Union[int, Tuple[int, int]]:
    """get neighbor position that have a bug on it
    if inner_depth is not None it will be depth / recursive aware

    Arguments:
        depth {int} -- the current depth
        y_pos {int} -- current y
        x_pos {int} -- current x
        bugs {set} -- current bugs state
        inner_depth {tuple} -- the inner depth location (center cell)
        y_count {int} -- the total y positions available
        x_count {int} -- the total x positions avaiable

    Returns:
        Union[int, Tuple[int, int] -- if no inner depth was provided,
                                      just a count of the total neighboring bugs.
                                      if inner depth was provided,
                                      it will return another int that represents the number
                                      of the neighboring depth that was visited. (+/- 1 from)

    """
    # set if another depth is found
    recursive_depth = None

    neighbors = get_neighbors(y_pos, x_pos)

    depth_neighbors = set()

    for neighbor in neighbors:
        if inner_depth:
            # check if neighbor is inner recursion
            if neighbor == inner_depth:
                # neighbors vary on position relative to inner recursion
                if y_pos < inner_depth[0]:
                    recursive_depth = depth + 1
                    recursive_y = 0
                    for recursive_x in range(x_count):
                        position = (recursive_depth, recursive_y, recursive_x)
                        depth_neighbors.add(position)
                elif y_pos > inner_depth[0]:
                    recursive_depth = depth + 1
                    recursive_y = y_count - 1
                    for recursive_x in range(x_count):
                        position = (recursive_depth, recursive_y, recursive_x)
                        depth_neighbors.add(position)
                elif x_pos < inner_depth[1]:
                    recursive_depth = depth + 1
                    recursive_x = 0
                    for recursive_y in range(y_count):
                        position = (recursive_depth, recursive_y, recursive_x)
                        depth_neighbors.add(position)
                elif x_pos > inner_depth[1]:
                    recursive_depth = depth + 1
                    recursive_x = x_count - 1
                    for recursive_y in range(y_count):
                        position = (recursive_depth, recursive_y, recursive_x)
                        depth_neighbors.add(position)
            # check up (outter depth)
            elif neighbor[0] < 0:
                recursive_depth = depth - 1
                position = (recursive_depth,
                            inner_depth[0] - 1, inner_depth[1])
                depth_neighbors.add(position)
            # check left
            elif neighbor[1] < 0:
                recursive_depth = depth - 1
                position = (recursive_depth,
                            inner_depth[0], inner_depth[1] - 1)
                depth_neighbors.add(position)
            # check down
            elif neighbor[0] >= y_count:
                recursive_depth = depth - 1
                position = (recursive_depth,
                            inner_depth[0] + 1, inner_depth[1])
                depth_neighbors.add(position)
            # check right
            elif neighbor[1] >= x_count:
                recursive_depth = depth - 1
                position = (recursive_depth,
                            inner_depth[0], inner_depth[1] + 1)
                depth_neighbors.add(position)
            else:
                position = (depth,
                            neighbor[0], neighbor[1])
                depth_neighbors.add(position)
        else:
            position = (depth,
                        neighbor[0], neighbor[1])
            depth_neighbors.add(position)

    intersect = bugs & depth_neighbors

    return len(intersect), recursive_depth


def repeat_biodiversity(bugs: set, y_count: int, x_count: int) -> int:
    """find the state that repeats and return its "rating"

    Arguments:
        bugs {set} -- bugs state
        y_count {int} -- total y available
        x_count {int} -- total x available

    Returns:
        int -- the rating of the repeated bug state
    """
    # historical account of previous patterns
    history = set()

    new_bugs = frozenset(bugs)
    while new_bugs not in history:

        # update history
        new_bugs = frozenset(new_bugs)
        history.add(new_bugs)

        new_bugs = spread(bugs, y_count, x_count)

        # update bugs
        bugs = new_bugs

    return sum(map(lambda bug: 2 ** (bug[1] * x_count + bug[2]), bugs))


def spread(bugs: set,
           y_count: int,
           x_count: int,
           is_recursive: bool = False,
           min_recursion: int = 0,
           max_recursion: int = 0) -> Union[int, Tuple[int, int, int]]:
    """spread bugs to neighboring cells

    Arguments:
        bugs {set} -- current bug state
        y_count {int} -- available y
        x_count {int} -- available x

    Keyword Arguments:
        is_recursive {bool} -- determines if this process is depth / recursive aware
                               (default: {False})
        min_recursion {int} -- min recursion (default: {0})
        max_recursion {int} -- max recusion (default: {0})

    Returns:
        Union[int, Tuple[int,int, int] -- if not recursive, just returns new bugs state
                                         otherwise it will also return the new
                                         min and max recursive depths
    """
    inner_depth = None
    if is_recursive:
        inner_depth = ((y_count - 1) // 2, (x_count - 1) // 2)

    depths = list(range(min_recursion, max_recursion + 1))
    new_bugs = set()
    while depths:
        depth = depths.pop()
        for y_position in range(y_count):
            for x_position in range(x_count):
                position = (depth, y_position, x_position)

                # skip this position if recursive
                if is_recursive and y_position == inner_depth[0] and x_position == inner_depth[1]:
                    continue

                neighbor_count, recursive_depth = neighbor_bugs(*position,
                                                                bugs,
                                                                inner_depth,
                                                                y_count,
                                                                x_count)
                is_bug = position in bugs

                if is_bug and is_recursive and recursive_depth:
                    # if a recursive_depth is reachable that
                    # is next to this bug but isn't in our range
                    # we need to consider it before compeletion
                    if recursive_depth < min_recursion:
                        min_recursion = recursive_depth
                        depths.append(recursive_depth)
                    if recursive_depth > max_recursion:
                        max_recursion = recursive_depth
                        depths.append(recursive_depth)

                if is_bug and neighbor_count == 1:
                    # bug lives
                    new_bugs.add(position)
                elif not is_bug and neighbor_count in {1, 2}:
                    # empty space is now infested
                    new_bugs.add(position)

    if is_recursive:
        return new_bugs, min_recursion, max_recursion
    else:
        return new_bugs


def spread_minutes(bugs: set, y_count: int, x_count: int, minutes: int) -> set:
    """spread bugs over a course of give time in minutes

    Arguments:
        bugs {set} -- bugs state
        y_count {int} -- available y
        x_count {int} -- available x
        minutes {int} -- total minutes to spread in

    Returns:
        set -- new bug state after x minutes pass
    """
    min_recursion = 0
    max_recursion = 0
    for _ in range(minutes):
        bugs, min_recursion, max_recursion = spread(
            bugs, y_count, x_count, True, min_recursion, max_recursion)

    return bugs


def read_bugs(file_input: TextIO) -> set:
    """read bug input and returns a starting state

    depth is 0 for all read inputs

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        set -- bug state
    """
    bugs = set()
    y_count = 0
    x_count = 0
    for y_position, line in enumerate(file_input):
        y_count += 1
        for x_position, character in enumerate(line.strip()):
            x_count = max(x_position + 1, x_count)
            if character == "#":
                # depth starts at 0
                position = (0, y_position, x_position)
                bugs.add(position)

    return bugs, y_count, x_count
