"""Part 2 Module"""
import click

from day_07.amplify import amp_checks


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_07.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))

    phase_settings = (5, 6, 7, 8, 9)
    strongest = amp_checks(codes, phase_settings)

    print(f"strongest signal was: {strongest}")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
