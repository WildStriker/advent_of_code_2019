"""Part 2 Module"""
import click

from day_10.map import parse_map, find_target


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_10.txt")
@click.option("--target", type=int, default=200)
def part_02(input_path, target):
    """Part 2"""
    with open(input_path) as file_input:
        asteriod_map = parse_map(file_input)

    coord = find_target(asteriod_map, target)
    print(f"{coord[1]} * 100 + {coord[0]} = {coord[1] * 100 + coord[0]}")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
