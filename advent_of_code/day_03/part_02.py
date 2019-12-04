"""Part 2 Module"""
import click

from day_03.intersect import fewest_steps, wire_coords


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_03.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        wire_1 = wire_coords(file_input.readline().split(","))
        wire_2 = wire_coords(file_input.readline().split(","))

    steps = fewest_steps(wire_1, wire_2)
    if steps:
        print(f"Fewest steps taken to an intersection is {steps}")
    else:
        print(f"There is no intersecting points")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
