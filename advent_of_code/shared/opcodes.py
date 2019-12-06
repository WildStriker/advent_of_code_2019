"""opcode and process logic"""
from typing import List, Tuple


def opcode_1(value_1: int, value_2: int) -> int:
    """opcode 1 returns the sum of two values


    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- sum of given values
    """
    return value_1 + value_2


def opcode_2(value_1: int, value_2: int) -> int:
    """opcode 2 returns the product of two values

    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- product of given values
    """
    return value_1 * value_2


def opcode_3() -> int:
    """prompts user for a number

    Returns:
        int -- returns valid integer
    """
    while True:
        try:
            selection = int(input("Input a number: "))
            return selection
        except ValueError:
            pass


def opcode_4(value: int):
    """prints given value"""
    print(value)


def opcode_5(value_1: int, value_2: int, instruction_pointer: int) -> int:
    """if the first parameter is non-zero it will pass the second parameter as
    the new instruction pointer

    otherwise it will iterate the pointer to the next instruction

    Arguments:
        value_1 {int} -- used in testing if non-zero
        value_2 {int} -- new instruction if value_1 is non-zero
        instruction_pointer {int} -- current pointer position

    Returns:
        int -- next pointer position
    """
    if value_1:
        return value_2
    return instruction_pointer + 3


def opcode_6(value_1: int, value_2: int, instruction_pointer: int) -> int:
    """if the first parameter is zero it will pass the second parameter as
    the new instruction pointer

    otherwise it will iterate the pointer to the next instruction

    Arguments:
        value_1 {int} -- used in testing if zero
        value_2 {int} -- new instruction if value_1 is zero
        instruction_pointer {int} -- current pointer position

    Returns:
        int -- next pointer position
    """
    if not value_1:
        return value_2
    return instruction_pointer + 3


def opcode_7(value_1: int, value_2: int) -> int:
    """compares value_1 is smaller than value_2

    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- returns 1 if value_1 is smaller, 0 if not
    """
    if value_1 < value_2:
        return 1
    return 0


def opcode_8(value_1: int, value_2: int) -> int:
    """compares value_1 is equal to value_2

    Arguments:
        value_1 {int} -- first value
        value_2 {int} -- second value

    Returns:
        int -- returns 1 if values are the same, 0 if not
    """
    if value_1 == value_2:
        return 1
    return 0


def get_instructions(code: int) -> Tuple[int, int, int]:
    """gets instructions from given code (opcode, and input modes)

    Arguments:
        code {int} -- code containing instructions

    Returns:
        Tuple[int, int, int] -- opcode, input_mode_1, input_mode_2
    """
    opcode = code % 100
    code = code // 100

    input_mode_1 = code % 10
    code = code // 10

    input_mode_2 = code % 10
    code = code // 10

    return opcode, input_mode_1, input_mode_2


def get_input(codes: List[int], input_position: int, input_mode: int) -> int:
    """retuns the input value based on input mode

    Arguments:
        codes {List[int]} -- list of all codes
        input_position {int} -- position input instruction is in
        input_mode {int} -- 1 for imediate mode, 0 for position mode

    Returns:
        int -- actual input value
    """
    # imediate mode (value at the actual position)
    if input_mode == 1:
        return codes[input_position]

    # position mode (value reference at another position)
    if input_mode == 0:
        position = codes[input_position]
        return codes[position]

    ValueError(f"Unknown Input Mode: {input_mode}")


def process(codes: List[int]) -> int:
    """process given inputs, returns result in the first position

    Arguments:
        codes {List[int]} -- list of opcodes and parameters

    Raises:
        ValueError: when an unknown instruction is given an error will occur

    Returns:
        int -- once opcode 99 is reach and the program terminates,
               results from the first position is returned
    """
    instruction_pointer = 0
    while True:
        # get instruction
        opcode, input_mode_1, input_mode_2 = get_instructions(
            codes[instruction_pointer])

        # terminate program
        if opcode == 99:
            return

        # get parameters and output position
        input_position_1 = instruction_pointer + 1
        input_position_2 = instruction_pointer + 2

        # run instruction set
        if opcode == 1:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            output_value = opcode_1(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            codes[output_position] = output_value

            instruction_pointer += 4
        elif opcode == 2:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            output_value = opcode_2(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            codes[output_position] = output_value

            instruction_pointer += 4
        elif opcode == 3:

            output_value = opcode_3()
            output_position = codes[instruction_pointer + 1]
            codes[output_position] = output_value

            instruction_pointer += 2
        elif opcode == 4:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)

            opcode_4(input_value_1)

            instruction_pointer += 2
        elif opcode == 5:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            instruction_pointer = opcode_5(
                input_value_1, input_value_2, instruction_pointer)
        elif opcode == 6:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            instruction_pointer = opcode_6(
                input_value_1, input_value_2, instruction_pointer)
        elif opcode == 7:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            output_value = opcode_7(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            codes[output_position] = output_value

            instruction_pointer += 4
        elif opcode == 8:
            input_value_1 = get_input(codes, input_position_1, input_mode_1)
            input_value_2 = get_input(codes, input_position_2, input_mode_2)

            output_value = opcode_8(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            codes[output_position] = output_value

            instruction_pointer += 4
        else:
            raise ValueError(f"unknown opcode: {opcode}")
