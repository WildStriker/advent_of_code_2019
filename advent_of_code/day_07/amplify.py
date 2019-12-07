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

        last_output = 0
        try:
            while True:
                for amp in amps:
                    next(amp)
                    _ok = amp.send(last_output)
                    last_output = next(amp)
        except StopIteration:
            pass
        results.append(last_output)

    return max(results)
