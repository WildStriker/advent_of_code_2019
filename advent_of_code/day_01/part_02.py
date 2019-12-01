"""Part 2 Module"""
import click

from day_01.calc import calc_fuel


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_01.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        total = 0
        for value in file_input:
            fuel_mass = int(value)
            while fuel_mass != 0:
                fuel_mass = calc_fuel(fuel_mass)
                total += fuel_mass

    print(total)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
