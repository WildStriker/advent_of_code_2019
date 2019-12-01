"""Part 01 Module"""
import click

from day_01.calc import calc_fuel


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_01.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        total = 0
        for value in file_input:
            mass = int(value)
            total += calc_fuel(mass)

    print(total)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
