"""Part 2 Module"""
import click

from day_06.orbit import distance, init_objects


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_06.txt")
@click.option("--mass-1", default="YOU")
@click.option("--mass-2", default="SAN")
def part_02(input_path, mass_1, mass_2):
    """Part 2"""
    with open(input_path) as file_input:
        objects = init_objects(file_input)

    total = distance(objects[mass_1], objects[mass_2])

    print(f"'{mass_1}' is {total} amount of hops from '{mass_2}'")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
