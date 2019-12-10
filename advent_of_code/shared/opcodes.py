"""opcode and process logic"""
from typing import Generator, List, Tuple, Union


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


def opcode_3(value: int) -> int:
    """returns value back

    Keyword Arguments:
        value {int} -- input value

    Returns:
        int -- returns value
    """
    return value


def opcode_4(value: int):
    """prints given value"""
    return value


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


def opcode_9(value_1: int, relative_base: int) -> int:
    """adjust relative base with given value

    Arguments:
        value_1 {int} -- value to increment base
        relative_base {int} -- current relative base

    Returns:
        int -- new relative base
    """
    return value_1 + relative_base


def get_instructions(code: int) -> Tuple[int, int, int]:
    """gets instructions from given code (opcode, and input modes)

    Arguments:
        code {int} -- code containing instructions

    Returns:
        Tuple[int, int, int, int] -- opcode, input_mode_1, input_mode_2, output_mode
    """
    opcode = code % 100
    code = code // 100

    input_mode_1 = code % 10
    code = code // 10

    input_mode_2 = code % 10
    code = code // 10

    output_mode = code % 10
    code = code // 10

    if code:
        raise ValueError(f"Unused Parameter {code}")

    return opcode, input_mode_1, input_mode_2, output_mode


def get_input(codes: List[int], input_position: int, relative_base: int, input_mode: int) -> int:
    """retuns the input value based on input mode

    Arguments:
        codes {List[int]} -- list of all codes
        input_position {int} -- position input instruction is in
        relative_base {int} -- relative position
        input_mode {int} -- mode to interupt where the value is
                            0 for position mode
                            1 for imediate mode
                            2 for relative mode

    Returns:
        int -- actual input value
    """
    # position mode (value reference at another position)
    if input_mode == 0:
        position = codes[input_position]
        return codes[position]

    # imediate mode (value at the actual position)
    if input_mode == 1:
        return codes[input_position]

    if input_mode == 2:
        position = relative_base + codes[input_position]
        return codes[position]

    ValueError(f"Unknown Input Mode: {input_mode}")


def set_output(codes: List[int],
               output_value: int,
               output_position: int,
               relative_base: int,
               output_mode: int):
    """set output value in list of instructions / codes

    Arguments:
        codes {List[int]} -- instructions list
        output_value {int} -- value being set
        output_position {int} -- output position
        relative_base {int} -- starting point for relative mode
        output_mode {int} -- output modes:
                             0 - positional (from base 0)
                             1 - relative (position offset from relative_base)

    Raises:
        ValueError: when unknown output mode is given
    """
    if output_mode == 0:
        codes[output_position] = output_value
    elif output_mode == 2:
        position = relative_base + output_position
        codes[position] = output_value
    else:
        raise ValueError("Unknown output mode: {output_mode}")


def process(codes: List[int]) -> Generator[Union[int, str], int, None]:
    """process given inputs, returns result in the first position

    Arguments:
        codes {List[int]} -- list of opcodes and parameters

    Raises:
        ValueError: when an unknown instruction is given an error will occur

    Yields:
        Generator[
            Union[int, str],
            int,
            None] -- yield values back as int for use as outputs.
                     when input is received an "ok" message is returned
    """
    instruction_pointer = 0
    relative_base = 0
    while True:
        # get instruction
        opcode, input_mode_1, input_mode_2, output_mode = get_instructions(
            codes[instruction_pointer])

        # terminate program
        if opcode == 99:
            return

        # get parameters and output position
        input_position_1 = instruction_pointer + 1
        input_position_2 = instruction_pointer + 2

        # run instruction set
        if opcode == 1:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            output_value = opcode_1(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            set_output(codes,
                       output_value,
                       output_position,
                       relative_base,
                       output_mode)

            instruction_pointer += 4
        elif opcode == 2:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            output_value = opcode_2(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            set_output(codes,
                       output_value,
                       output_position,
                       relative_base,
                       output_mode)

            instruction_pointer += 4
        elif opcode == 3:
            value = yield
            yield "ok"
            output_value = opcode_3(value)
            output_position = codes[instruction_pointer + 1]
            output_mode = input_mode_1
            set_output(codes,
                       output_value,
                       output_position,
                       relative_base,
                       output_mode)

            instruction_pointer += 2
        elif opcode == 4:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)

            yield opcode_4(input_value_1)

            instruction_pointer += 2
        elif opcode == 5:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            instruction_pointer = opcode_5(input_value_1,
                                           input_value_2,
                                           instruction_pointer)
        elif opcode == 6:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            instruction_pointer = opcode_6(input_value_1,
                                           input_value_2,
                                           instruction_pointer)
        elif opcode == 7:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            output_value = opcode_7(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            set_output(codes,
                       output_value,
                       output_position,
                       relative_base,
                       output_mode)

            instruction_pointer += 4
        elif opcode == 8:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)
            input_value_2 = get_input(codes,
                                      input_position_2,
                                      relative_base,
                                      input_mode_2)

            output_value = opcode_8(input_value_1, input_value_2)
            output_position = codes[input_position_2 + 1]
            set_output(codes,
                       output_value,
                       output_position,
                       relative_base,
                       output_mode)

            instruction_pointer += 4
        elif opcode == 9:
            input_value_1 = get_input(codes,
                                      input_position_1,
                                      relative_base,
                                      input_mode_1)

            relative_base = opcode_9(input_value_1, relative_base)

            instruction_pointer += 2
        else:
            raise ValueError(f"unknown opcode: {opcode}")
