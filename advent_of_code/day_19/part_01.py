"""Part 1 Module"""
import click

from day_19.beam import tractor_beam
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_19.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    total = tractor_beam(codes, 49, 49)
    print(total)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
