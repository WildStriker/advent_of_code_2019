"""Part 2 Module"""
import click

from shared.opcodes import process


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_05.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))

    processing = process(codes)
    next(processing)
    _ok = processing.send(5)

    for output in processing:
        print(output)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
