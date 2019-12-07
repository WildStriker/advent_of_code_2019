"""Part 1 Module"""
import click

from shared.opcodes import process


@click.command()
@click.option('--input', "input_path", type=click.Path(exists=True), default="inputs\\day_02.txt")
@click.option("--noun", type=int, default=12)
@click.option("--verb", type=int, default=2)
def part_01(input_path, noun, verb):
    """Part 1"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))

    # replace positions 1 and 2
    codes[1] = noun
    codes[2] = verb

    processing = process(codes)
    for _ in processing:
        pass

    print(f"result is {codes[0]}")


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
