"""Part 1 Module"""
import click

from day_03.intersect import closest_intersect, wire_coords


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_03.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        wire_1 = wire_coords(file_input.readline().split(","))
        wire_2 = wire_coords(file_input.readline().split(","))

    distance = closest_intersect(wire_1, wire_2)
    if distance:
        print(f"Closest intersecting point distance from center is {distance}")
    else:
        print(f"There is no intersecting points")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
