"""Part 2 Module"""
import click

from day_15.repair import fill_oxygen
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_15.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    minutes = fill_oxygen(codes)
    print(minutes)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
