"""Part 2 Module"""
import click

from day_02.process import process


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_02.txt")
@click.option("--target-output", "target", type=int, default=19690720)
def part_02(input_path, target):
    """Part 2"""
    with open(input_path) as file_input:
        init_codes = list(map(int, file_input.read().split(",")))

    # loop through each possible noun and verb (0-99)
    for noun in range(100):
        for verb in range(100):
            codes = init_codes.copy()
            # update starting "noun" and "verb"
            codes[1] = noun
            codes[2] = verb
            result = process(codes)
            if result == target:
                print(f"100 * {noun} + {verb} = {100 * noun + verb}")
                return


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter