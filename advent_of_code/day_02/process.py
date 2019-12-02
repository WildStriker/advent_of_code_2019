"""opt code and process logic"""
from typing import List


def opt_1(value_1: int, value_2: int) -> int:
    """opt code 1 returns the sum of two values


    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- sum of given values
    """
    return value_1 + value_2


def opt_2(value_1: int, value_2: int) -> int:
    """opt code 2 returns the product of two values

    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- product of given values
    """
    return value_1 * value_2


def process(codes: List[int]) -> int:
    """process given inputs, returns result in the first position

    Arguments:
        codes {List[int]} -- list of opt codes and parameters

    Raises:
        ValueError: when an unknown instruction is given an error will occur

    Returns:
        int -- once opt code 99 is reach and the program terminates,
               results from the first position is returned
    """
    read_position = 0
    while True:
        # get instruction
        opt_code = codes[read_position]

        # terminate program
        if opt_code == 99:
            return codes[0]

        # get parameters and output position
        input_position_1 = codes[read_position + 1]
        input_position_2 = codes[read_position + 2]
        output_position = codes[read_position + 3]

        input_value_1 = codes[input_position_1]
        input_value_2 = codes[input_position_2]

        # run instruction set
        if opt_code == 1:
            output_value = opt_1(input_value_1, input_value_2)
        elif opt_code == 2:
            output_value = opt_2(input_value_1, input_value_2)
        else:
            raise ValueError(f"unknown opt code: {opt_code}")

        # output results
        codes[output_position] = output_value

        # next instruction set
        read_position += 4
