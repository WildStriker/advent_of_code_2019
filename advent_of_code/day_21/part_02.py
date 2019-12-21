"""Part 2 Module"""
import click

from day_21.ascii import hull_damage
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_21.txt")
@click.option('--debug', is_flag=True)
def part_02(input_path, debug):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    if debug:
        total = hull_damage(codes)
    else:
        # tile 1, 2, or 3 is a hole and 4 is not
        # and tile 5 or 8 is not
        inputs = list(
            "NOT A T\n"
            "OR T J\n"
            "NOT B T\n"
            "OR T J\n"
            "NOT C T\n"
            "OR T J\n"
            "AND D J\n"
            "AND E T\n"
            "OR H T\n"
            "AND T J\n"
            "RUN\n")
        total = hull_damage(codes, inputs)

    print(total)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
