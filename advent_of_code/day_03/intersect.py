"""logic for wire intersections"""
from typing import Dict, List

from shared.distance import manhattan_distance


def wire_coords(directions: List[str]) -> Dict[tuple, int]:
    """generate coords to represent wire

    Arguments:
        directions {List[str]} -- list of directions from the central point

    Raises:
        ValueError: raised when an invalid direction is given

    Returns:
        Dict[tuple, int] -- coords for wire
    """

    coords: Dict[tuple, int] = {}

    current_x = 0
    current_y = 0

    steps = 0

    for direction_amount in directions:
        direction = direction_amount[0]
        amount = int(direction_amount[1:])

        for _ in range(amount):
            steps += 1
            if direction == "U":
                current_y += 1
            elif direction == "R":
                current_x += 1
            elif direction == "D":
                current_y -= 1
            elif direction == "L":
                current_x -= 1
            else:
                raise ValueError(f"Unknown Direction {direction}")

            # coordinates used as key, store steps taken
            current_coord = (current_x, current_y)

            coords[current_coord] = steps
    return coords


def closest_intersect(wire_1: Dict[tuple, int], wire_2: Dict[tuple, int]) -> int:
    """returns the closest wire intersection to the central point starting at (0, 0)

    Arguments:
        wire_1 {Dict[tuple, int]} -- coords representing the first wire
        wire_2 {Dict[tuple, int]} -- coords representing the second wire

    Returns:
        int -- the closest intersecting point, returns None if no intersections
    """

    center = (0, 0)
    closest_point = None

    intersections = wire_1.keys() & wire_2.keys()

    for intersection in intersections:
        distance = manhattan_distance(center, intersection)

        if not closest_point or distance < closest_point:
            closest_point = distance

    return closest_point


def fewest_steps(wire_1: Dict[tuple, int], wire_2: Dict[tuple, int]) -> int:
    """find and returns the fewest steps to an intersection

    Arguments:
        wire_1 {Dict[tuple, int]} -- coords representing the first wire
        wire_2 {Dict[tuple, int]} -- coords representing the second wire

    Returns:
        int -- the fewest steps to an intersection
    """
    fewest = None

    intersections = wire_1.keys() & wire_2.keys()

    for intersection in intersections:
        steps_taken = wire_1[intersection] + wire_2[intersection]
        if not fewest or steps_taken < fewest:
            fewest = steps_taken

    return fewest
