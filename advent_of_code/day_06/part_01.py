"""Part 1 Module"""
import click

from day_06.orbit import init_objects, orbit_count


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_06.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        objects = init_objects(file_input)

    count = orbit_count(objects)

    print(f"There is {count} objects in orbit")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
