"""distance related helper functions"""


def manhattan_distance(coord_1: tuple, coord_2: tuple):
    """find distance between two points"""
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])
