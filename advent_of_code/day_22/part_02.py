"""Part 2 Module"""
import click

from day_22.deck import get_instructions, find_iter


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_22.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        instructions = get_instructions(file_input)

    value = find_iter(instructions, 119315717514047, 101741582076661, 2020)
    print(value)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
