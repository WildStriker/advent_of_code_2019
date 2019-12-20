"""Part 2 Module"""
import click

from day_18.path import get_shortest, read_quadrants


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_18.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        quad_1, quad_2, quad_3, quad_4 = read_quadrants(file_input)

    steps_1 = get_shortest(*quad_1)
    steps_2 = get_shortest(*quad_2)
    steps_3 = get_shortest(*quad_3)
    steps_4 = get_shortest(*quad_4)
    print(steps_1 + steps_2 + steps_3 + steps_4)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
