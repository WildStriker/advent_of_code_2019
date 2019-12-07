"""Part 1 Module"""
import click

from day_07.amplify import amp_checks


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_07.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))

    phase_settings = (0, 1, 2, 3, 4)
    strongest = amp_checks(codes, phase_settings)

    print(f"strongest signal was: {strongest}")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
