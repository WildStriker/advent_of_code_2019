"""Part 1 Module"""
import click

from day_25.ascii import navigate
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_25.txt")
@click.option('--debug', is_flag=True)
def part_01(input_path, debug):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    if debug:
        navigate(codes)
    else:
        inputs = list(
            "south\n"
            "south\n"
            "take candy cane\n"
            "north\n"
            "west\n"
            "west\n"
            "take astrolabe\n"
            "east\n"
            "east\n"
            "north\n"
            "east\n"
            "take food ration\n"
            "south\n"
            "east\n"
            "south\n"
            "east\n"
            "take space law space brochure\n"
            "north\n"
            "west\n")
        navigate(codes, inputs)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
