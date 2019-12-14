"""Part 2 Module"""
import click

from day_14.resource import count_fuel, parse_input


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_14.txt")
@click.option("--ore", type=int, default=1000000000000)
def part_02(input_path, ore):
    """Part 2"""
    with open(input_path) as file_input:
        resource_map = parse_input(file_input)

    count = count_fuel(resource_map, ore)
    print(count)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
