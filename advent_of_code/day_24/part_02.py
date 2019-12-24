"""Part 2 Module"""
import click

from day_24.bugs import read_bugs, spread_minutes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_24.txt")
@click.option("--minutes", type=int, default=200)
def part_02(input_path, minutes):
    """Part 2"""
    with open(input_path) as file_input:
        bugs, y_count, x_count = read_bugs(file_input)

    bugs = spread_minutes(bugs, y_count, x_count, minutes)

    print(f"After {minutes} minutes there is a total of {len(bugs)} bugs")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
