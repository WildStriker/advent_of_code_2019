"""Part 1 Module"""
import click

from day_04.secure import combinations


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_04.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        start, end = list(map(int, file_input.read().split("-")))

    total = combinations(start, end, False)
    print(total)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
