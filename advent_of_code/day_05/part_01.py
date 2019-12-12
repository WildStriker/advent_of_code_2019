"""Part 1 Module"""
import click

from shared.opcodes import process, read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_05.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    processing = process(codes)
    next(processing)
    _ok = processing.send(1)

    for output in processing:
        print(output)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
