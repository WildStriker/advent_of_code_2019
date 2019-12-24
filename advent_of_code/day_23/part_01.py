"""Part 1 Module"""
import click

from day_23.network import communicate
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_23.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    address, x_portion, y_portion = communicate(codes)

    print(f"{address} is outside address range")
    print(f"Tried to send packet x: {x_portion} and y: {y_portion}")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
