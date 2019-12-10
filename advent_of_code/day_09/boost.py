"""amplify logic module"""
from typing import List

from shared.opcodes import process


def run(codes: List[int], phase: int = None):
    """run given input with provided phase

    Arguments:
        codes {List[int]} -- instruction set

    Keyword Arguments:
        phase {int} -- optinal input (default: {None})
    """
    boosting = process(codes)

    if phase is not None:
        next(boosting)
        _ok = boosting.send(phase)

    for output in boosting:
        print(output)
