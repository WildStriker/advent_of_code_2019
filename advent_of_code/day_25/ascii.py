"""ascii intcode logic"""
import collections
from dataclasses import dataclass, field
from typing import DefaultDict, Deque

from shared.opcodes import process


@dataclass
class Droid:
    """control flow of inputs to intcode machine"""
    inputs: Deque = field(default_factory=collections.deque)

    def droid_input(self):
        """input instruction to navigate through the different rooms"""
        current_input = ""
        if not self.inputs:
            while current_input == "":
                current_input = input("Command: ").strip()
                for letter in current_input:
                    self.inputs.append(letter)
                self.inputs.append("\n")
        next_letter = self.inputs.popleft()
        return ord(next_letter)


def navigate(codes: DefaultDict[int, int], inputs: list = None):
    """navigate bot

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions

    Keyword Arguments:
        inputs {list} -- given params
    """
    if inputs:
        droid = Droid(collections.deque(inputs))
    else:
        droid = Droid()

    droid_logic = process(codes, droid.droid_input)

    outputs = []
    for output in droid_logic:
        if output == 10:
            print("".join(outputs))
            outputs = []
        else:
            outputs.append(chr(output))
