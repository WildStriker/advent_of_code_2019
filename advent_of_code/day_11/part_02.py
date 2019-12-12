"""Part 2 Module"""
import click

from day_11.painter import WHITE, render_painted
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_11.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    render_painted(codes, {(0, 0): WHITE})


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
