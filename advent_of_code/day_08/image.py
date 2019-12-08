"""image logic module"""
from collections import Counter
from typing import List

BLACK = 0
WHITE = 1
TRANSPARENT = 2


def validate(digits: List[int], wide: int, tall: int) -> int:
    """validate image is not corrupted by taking the layer with the fewest BLACK pixels
    and calculate total WHITE * total TRANSPARENT pixels

    Arguments:
        digits {List[int]} -- list of all pixels
        wide {int} -- length of image
        tall {int} -- height of image

    Returns:
        int -- results of total WHITE pixels * total TRANSPARENT pixels
    """

    # only care about total pixels in a layer so get this now
    step = wide * tall

    # count each layers pixels (by pixel type)
    layer_counts = []
    for start in range(0, len(digits), step):
        layer = digits[start:start + step]

        count = Counter(layer)
        layer_counts.append(count)

    # find layer with the least BLACK pixels
    count = min(layer_counts, key=lambda count: count[BLACK])

    return count[WHITE] * count[TRANSPARENT]


def image_translate(digit: int) -> str:
    """output digit to terminal in a more readable format

    Arguments:
        digit {int} -- digit being translated

    Returns:
        str -- translated output image
    """
    # "white" pixel and therefore "on"
    if digit == WHITE:
        return "*"
    return " "


def render(digits: List[int], wide: int, tall: int):
    """render pixels layer by layer overwritting only the transparent layers

    Arguments:
        digits {List[int]} -- list of pixels
        wide {int} -- length of image
        tall {int} -- height of image
    """
    # init image pixels (starts as transparent)
    image = [[TRANSPARENT]*wide for _ in [TRANSPARENT]*tall]

    index = 0
    total_digits = len(digits)
    while index < total_digits:
        for pos_y in range(tall):
            for pos_x in range(wide):
                pixel = digits[index]
                if image[pos_y][pos_x] == TRANSPARENT:
                    image[pos_y][pos_x] = pixel
                index += 1

    for row in image:
        print(''.join(map(image_translate, row)))
