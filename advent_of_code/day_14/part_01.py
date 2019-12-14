"""Part 1 Module"""
import click

from day_14.resource import count_ore, parse_input


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_14.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        resource_map = parse_input(file_input)

    count = count_ore(resource_map)
    print(count)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
