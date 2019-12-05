"""secure logic"""


def combinations(start: int, end: int, repeat_twice: bool) -> int:
    """count all valid combinations in range

    Arguments:
        start {int} -- starting range
        end {int} -- ending range
        repeat_twice {bool} -- if True repeating values must occur exactly twice (one time)

    Returns:
        int -- total found valid combinations
    """
    total = 0
    for number in range(start, end + 1):
        previous_digit = None

        is_ordered = True

        is_repeating = False
        valid_repeating = False
        adjacent_repeat = False

        # iterate through each digit (right to left)
        # check that it is ordered smallest to largest
        # and at least two digits repeat and are adjacent
        # if repeat_twice is True, then this is only valid if the number repeats only twice
        digit = number % 10
        iterate_number = number // 10
        while iterate_number:
            previous_digit = digit
            digit = iterate_number % 10
            iterate_number = iterate_number // 10

            # digit order flag
            if digit > previous_digit:
                is_ordered = False
                break

            # repeating flags
            if previous_digit == digit:
                if repeat_twice and is_repeating:
                    # looking for two digits only, not valid
                    valid_repeating = False
                else:
                    is_repeating = True
                    valid_repeating = True

            # check that we have a valid repeating number when
            # previous digit no longer matches, or no more digits left
            if previous_digit != digit or not iterate_number:
                if is_repeating and valid_repeating:
                    adjacent_repeat = True
                # reset repeating flags
                is_repeating = False
                valid_repeating = False

        if adjacent_repeat and is_ordered:
            total += 1

    return total
