"""amplify logic module"""
import itertools
from typing import List

from shared.opcodes import process


def amp_checks(codes: List[int], phase_settings: List[int]) -> int:
    """check all possible phase settings for optimal settings for amplifiers

    Arguments:
        codes {List[int]} -- original list of codes to start on each amp
        phase_settings {List[int]} -- known phase settings (not in a particular order)

    Returns:
        int -- returns the largest possible output with known phase settings
    """

    # list of every result from all sequences
    results = []

    sequences = itertools.permutations(phase_settings)

    for sequence in sequences:
        last_output = 0
        amps = []
        for phase_setting in sequence:
            # run through amp with a phase settings and last output from previous amp
            amp_codes = codes.copy()
            amp = process(amp_codes)
            next(amp)
            _ok = amp.send(phase_setting)
            amps.append(amp)

        next(amps[0])
        _ok = amps[0].send(0)
        try:
            while True:
                for index, amp in enumerate(amps):
                    last_output = next(amps[index])
                    if index + 1 >= len(amps):
                        next(amps[0])
                        amps[0].send(last_output)
                    else:
                        next(amps[index + 1])
                        _ok = amps[index + 1].send(last_output)
        except StopIteration:
            pass
        results.append(last_output)

    return max(results)
