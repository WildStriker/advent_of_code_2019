"""calculate signal output"""
from typing import List, TextIO


def phase_shift(signal: List[int]) -> List[int]:
    """run signal through phase calculations

    Arguments:
        signal {List[int]} -- original signal

    Returns:
        List[int] -- output results
    """
    pattern = [0, 1, 0, -1]
    phases = 100
    signal_length = len(signal)
    pattern_length = len(pattern)
    input_list = signal.copy()
    output_list = [None] * len(input_list)
    for _ in range(phases):
        for index in range(signal_length):
            total = 0
            input_index = 0

            index_pattern = 0
            repeat = index
            # skip all repeated 0s
            if pattern[index_pattern] == 0:
                input_index += repeat
            elif repeat:
                # tally results
                total += sum(input_list[input_index:input_index +
                                        repeat]) * pattern[index_pattern]
                input_index += repeat

            repeat += 1
            index_pattern += 1
            while input_index < signal_length:
                # skip all repeated 0s
                if pattern[index_pattern] == 0:
                    input_index += repeat
                else:
                    total += sum(input_list[input_index:input_index +
                                            repeat]) * pattern[index_pattern]
                    input_index += repeat

                index_pattern += 1
                if index_pattern >= pattern_length:
                    index_pattern = 0
            output_list[index] = abs(total) % 10
        input_list = output_list.copy()

    return output_list


def reverse_sum(signal: List[int]) -> List[int]:
    """once offset is skipped only a small remaining digits are left

    from given example:
    Input signal: 12345678

    1*1  + 2*0  + 3*-1 + 4*0  + 5*1  + 6*0  + 7*-1 + 8*0  = 4
    1*0  + 2*1  + 3*1  + 4*0  + 5*0  + 6*-1 + 7*-1 + 8*0  = 8
    1*0  + 2*0  + 3*1  + 4*1  + 5*1  + 6*0  + 7*0  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*1  + 5*1  + 6*1  + 7*1  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*0  + 5*1  + 6*1  + 7*1  + 8*1  = 6
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*1  + 7*1  + 8*1  = 1
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*1  + 8*1  = 5
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*0  + 8*1  = 8

    we can see from the last index only the last value remains
    then going up to the 4th index / halfway point we see it is
    a running total % 10
    (8) % 10 = 8
    (8 + 7) % 10 = 5
    (8 + 7 + 6) % 10 = 1
    (8 + 7 + 6 + 5) % 10 = 6

    Arguments:
        signal {List[int]} -- signal, this is minus the offset amount

    Returns:
        List[int] -- output results
    """
    output_list = signal.copy()
    start = len(signal) - 1
    phase = 100
    for _ in range(phase):
        total = 0
        for index in range(start, -1, -1):
            total += output_list[index]
            output_list[index] = total % 10
    return output_list


def get_signal(file_input: TextIO) -> List[int]:
    """read input signal from file stream

    Arguments:
        file_input {TextIO} -- text stream

    Returns:
        int -- signal list, separated by digit
    """
    signal = []
    for digit in file_input.readline():
        signal.append((int(digit)))
    return signal
