"""Part 2 Module"""
import copy

import click

from shared.opcodes import process, read_codes


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_02.txt")
@click.option("--target-output", "target", type=int, default=19690720)
def part_02(input_path, target):
    """Part 2"""
    with open(input_path) as file_input:
        init_codes = read_codes(file_input)

    # loop through each possible noun and verb (0-99)
    for noun in range(100):
        for verb in range(100):
            codes = copy.copy(init_codes)
            # update starting "noun" and "verb"
            codes[1] = noun
            codes[2] = verb

            processing = process(codes)
            for _ in processing:
                pass

            if codes[0] == target:
                print(f"100 * {noun} + {verb} = {100 * noun + verb}")
                return


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
