"""Part 1 Module"""
import click

from day_16.signal import get_signal, phase_shift


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_16.txt")
def part_01(input_path):
    """Part 1"""
    with open(input_path) as file_input:
        signal = get_signal(file_input)

    output = phase_shift(signal)
    print(''.join(map(str, output[:8])))


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
