"""Part 1 Module"""
import click

from day_10.map import count_visible, parse_map


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_10.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        asteriod_map = parse_map(file_input)

    visible = count_visible(asteriod_map)
    print(visible)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
