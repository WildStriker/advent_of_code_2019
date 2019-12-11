"""mapping asteriods"""
import collections
import math
from typing import Dict, TextIO

from shared.distance import manhattan_distance


def parse_map(file_input: TextIO) -> Dict[tuple, dict]:
    """given file input init asteriod dictionary

    collection of coords to an empty dict

    This will later be expanded to a rad/angle and the related
    asteriod coords

    Arguments:
        file_input {TextIO} -- file stream

    Returns:
        Dict[tuple, dict] -- collection of asteriods
    """
    asteriods = {}
    y_pos = 0
    for line in file_input:
        x_pos = 0
        for char in line:
            if char == "#":
                position = (y_pos, x_pos)
                asteriods[position] = {}
            x_pos += 1
        y_pos += 1
    return asteriods


def init_arcs(asteriods: Dict[tuple, Dict[float, set]]):
    """initialize asteriod dictionary with a collection of
    coordinators that share the same angle to a given asteriod (coords)

    Arguments:
        asteriods {Dict[tuple, Dict[float, set]]} -- collection of asteriods and related angles
    """
    for coord, visible in asteriods.items():
        for other_coord in asteriods.keys():
            if coord != other_coord:
                collection = visible.setdefault(
                    get_arc(coord, other_coord), set())
                collection.add(other_coord)


def get_arc(coord1: tuple, coord2: tuple) -> float:
    """get the arc tangent of two coords (in radians)

    Arguments:
        coord1 {tuple} -- first coords
        coord2 {tuple} -- second coords

    Returns:
        float -- arc tangent of the two given coords
    """
    return math.atan2(coord1[0] - coord2[0], coord1[1] - coord2[1])


def count_visible(asteriods: Dict[tuple, Dict[float, set]]) -> int:
    """get the count of the largest collection of rads / "visible" asteriods

    Arguments:
        asteriods {Dict[tuple, Dict[float, set]]} -- asteriod collection

    Returns:
        int -- largest "visible" asteriod count
    """
    init_arcs(asteriods)
    return max(map(len, asteriods.values()))


def find_target(asteriods: Dict[tuple, Dict[float, set]], vaporized_count: int) -> tuple:
    """find and return the asteriod coords expected to be destoryed at a certain count

    Arguments:
        asteriods {Dict[tuple, Dict[float, set]]} -- collection of asteriods
        vaporized_count {int} -- targeted count to look for

    Returns:
        tuple -- coordinations of the asteriod being destoryed at the target count
    """
    # init counts
    init_arcs(asteriods)

    # get base (highest visible count)
    base_coords, base = max(asteriods.items(), key=lambda item: len(item[1]))

    # sort rads listing
    targets = sorted(base.items(), key=lambda collection: collection[0])

    # sort coords closet to base
    for index, target in enumerate(targets):
        sorted_list = list(target[1])
        sorted_list = sorted(sorted_list,
                             key=lambda coords: manhattan_distance(
                                 base_coords, coords),
                             reverse=True)
        targets[index] = (target[0], sorted_list)

    # convert to deque
    targets = collections.deque(targets)

    # find starting point
    start_point = get_arc((1, 1), (0, 1))
    while targets[0][0] < start_point:
        targets.rotate(-1)

    # start vaporizing asteriods!
    count = 0
    while targets:
        _rad, asteriods = targets[0]
        destroy = asteriods.pop()
        count += 1
        if count == vaporized_count:
            return destroy

        if asteriods:
            targets.rotate(-1)
        else:
            targets.popleft()
