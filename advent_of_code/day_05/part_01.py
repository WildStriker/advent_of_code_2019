"""Part 1 Module"""
import click

from day_05.opcodes import process


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_05.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))

    process(codes)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
