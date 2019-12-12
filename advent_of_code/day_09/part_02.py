"""Part 2 Module"""
import click

from day_09.boost import run
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_09.txt")
@click.option("--phase", type=int, default=2)
def part_02(input_path, phase):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    run(codes, phase)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
