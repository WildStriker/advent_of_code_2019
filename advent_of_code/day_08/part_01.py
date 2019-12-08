"""Part 1 Module"""
import click

from day_08.image import validate


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_08.txt")
@click.option("--wide", type=int, default=25)
@click.option("--tall", type=int, default=6)
def part_01(input_path, wide, tall):
    """Part 1"""
    with open(input_path) as file_input:
        digits = [int(digit) for digit in file_input.read()]

    result = validate(digits, wide, tall)

    print(result)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
