"""tractor beam logic"""
import copy
from dataclasses import dataclass
from typing import DefaultDict

from shared.opcodes import process


@dataclass
class TractorInput:
    """Tractor Beam Input State"""
    is_x_input: bool = False
    current_y: int = 0
    current_x: int = 0

    def inputs(self) -> int:
        """feed inputs to intcode machine"""
        self.is_x_input = not self.is_x_input
        if self.is_x_input:
            return self.current_x
        return self.current_y


def tractor_beam(codes: DefaultDict[int, int], max_y: int, max_x: int) -> int:
    """count area effected by tractor beam

    Arguments:
        codes {DefaultDict[int, int]} -- intcode machine instructions
        max_y {int} -- area max y we are considering
        max_x {int} -- area max x we are considering

    Returns:
        int -- total count
    """
    tractor_input = TractorInput()

    total = 0

    start_x = 0
    min_row_count = 1
    current_row_count = 0

    first_x = True
    output = []
    while tractor_input.current_y < max_y:
        beam = process(copy.copy(codes), tractor_input.inputs)
        for status in beam:
            if status == 1:
                if first_x:
                    start_x = tractor_input.current_x + 1
                    first_x = False
                    repeat_count = min(
                        min_row_count, max_x - tractor_input.current_x)
                    output += ["#"] * repeat_count
                    current_row_count += repeat_count
                    tractor_input.current_x += repeat_count - 1

                else:
                    output.append("#")
                    current_row_count += 1
            else:
                output.append(".")

            if tractor_input.current_x >= start_x + int(min_row_count * 1.25) \
                    or tractor_input.current_x >= max_x:
                print("".join(output))
                if current_row_count == 0:
                    return total
                tractor_input.current_x = start_x
                output = ["."] * start_x

                tractor_input.current_y += 1
                first_x = True
                min_row_count = max(min_row_count, current_row_count)
                total += current_row_count
                current_row_count = 0
            else:
                tractor_input.current_x += 1


def fit(codes: DefaultDict[int, int], width, height: int) -> int:
    """find position in tractor beam that will fit our width and height

    Arguments:
        codes {DefaultDict[int, int]} -- intcode machine instructions
        width {[type]} -- min x area
        height {int} -- min y area

    Returns:
        int -- computed value based on top left area we can fit in
    """
    tractor_bottom_left = TractorInput()
    tractor_bottom_left.current_x = 1
    tractor_bottom_left.current_y = height
    tractor_top_right = TractorInput()

    while True:
        beam_bottom_left = process(
            copy.copy(codes), tractor_bottom_left.inputs)
        bottom_status = next(beam_bottom_left)
        if bottom_status:
            tractor_top_right.current_x = tractor_bottom_left.current_x + width - 1
            tractor_top_right.current_y = tractor_bottom_left.current_y - height + 1
            beam_top_right = process(
                copy.copy(codes), tractor_top_right.inputs)
            top_status = next(beam_top_right)
            if top_status:
                break
            tractor_bottom_left.current_y += 1

        tractor_bottom_left.current_x += 1

    return tractor_bottom_left.current_x * 10000 + tractor_top_right.current_y
