"""Part 2 Module"""
import click

from day_13.arcade import play
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_13.txt")
@click.option("--quarters", type=int, default=2)
@click.option('--human', is_flag=True)
def part_02(input_path, quarters, human):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    codes[0] = quarters
    play(codes, human)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
