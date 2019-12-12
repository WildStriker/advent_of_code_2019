"""Part 1 Module"""
import click

from day_11.painter import count_painted
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_11.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    count = count_painted(codes)
    print(count)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
