"""ascii intcode logic"""
import collections
from dataclasses import dataclass, field
from typing import DefaultDict, Deque

from shared.opcodes import process


@dataclass
class SpringDroid:
    """control flow of inputs to intcode machine"""
    inputs: Deque = field(default_factory=collections.deque)

    def droid_input(self):
        """if no input given, prompts user for inputs
        this is continous until a "WALK" or "RUN" input is given"""
        current_input = ""
        if not self.inputs:
            while current_input not in {"WALK", "RUN"}:
                current_input = input("Next Instruction: ")
                for letter in current_input:
                    self.inputs.append(letter)
                self.inputs.append("\n")
        next_letter = self.inputs.popleft()
        return ord(next_letter)


def hull_damage(codes: DefaultDict[int, int], inputs: list = None) -> int:
    """hull damage report.  given valid spring droid inputs bot will report
    hull damage.  Otherwise it will output if the droid is stuck in a hole.

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions

    Keyword Arguments:
        inputs {list} -- spring board instructions, if not given user will be prompted

    Returns:
        int -- [description]
    """
    if inputs:
        droid = SpringDroid(collections.deque(inputs))
    else:
        droid = SpringDroid()

    droid_logic = process(codes, droid.droid_input)

    outputs = []
    for output in droid_logic:
        if output > 255:
            return output

        if output == 10:
            print("".join(outputs))
            outputs = []
        else:
            outputs.append(chr(output))
