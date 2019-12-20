"""Part 1 Module"""
import click

from day_18.path import get_shortest, read_input


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_18.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        start, path, keys, doors = read_input(file_input)

    steps = get_shortest(start, path, keys, doors)
    print(steps)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
