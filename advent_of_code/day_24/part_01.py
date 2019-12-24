"""Part 1 Module"""
import click

from day_24.bugs import read_bugs, repeat_biodiversity


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_24.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        bugs, y_count, x_count = read_bugs(file_input)

    rating = repeat_biodiversity(bugs, y_count, x_count)

    print(f"Biodiverstiy rating is {rating}")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
