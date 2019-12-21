"""Part 1 Module"""
import click

from day_21.ascii import hull_damage
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_21.txt")
@click.option('--debug', is_flag=True)
def part_01(input_path, debug):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    if debug:
        total = hull_damage(codes)
    else:
        inputs = list("NOT C J\n"
                      "AND D J\n"
                      "NOT A T\n"
                      "OR T J\n"
                      "WALK\n")
        total = hull_damage(codes, inputs)

    print(total)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
