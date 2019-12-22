"""Part 1 Module"""
import click

from day_22.deck import shuffle, get_instructions


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_22.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        instructions = get_instructions(file_input)
        deck = list(range(10007))
        deck = shuffle(instructions, deck)

    print(deck.index(2019))


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
