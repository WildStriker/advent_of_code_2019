"""amplify logic module"""
from typing import DefaultDict

from shared.opcodes import process


def run(codes: DefaultDict[int, int], phase: int = None):
    """run given input with provided phase

    Arguments:
        codes {DefaultDict[int, int]} -- instruction set

    Keyword Arguments:
        phase {int} -- optinal input (default: {None})
    """
    boosting = process(codes)

    if phase is not None:
        next(boosting)
        _ok = boosting.send(phase)

    for output in boosting:
        print(output)
