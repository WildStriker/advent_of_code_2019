"""Part 2 Module"""
import click

from day_20.portals import read_input, get_shortest


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_20.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        start, goal, path, outter_portals, inner_portals = read_input(file_input)

    steps = get_shortest(start, goal, path, outter_portals, inner_portals, True)
    print(steps)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
