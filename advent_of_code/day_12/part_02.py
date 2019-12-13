"""Part 2 Module"""
import click

from day_12.gravity import find_repeat, parse_input


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_12.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        moons = parse_input(file_input)

    steps = find_repeat(moons)
    print(steps)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
