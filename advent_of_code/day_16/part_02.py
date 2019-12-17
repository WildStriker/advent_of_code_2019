"""Part 2 Module"""
import click

from day_16.signal import get_signal, reverse_sum


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_16.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        signal = get_signal(file_input) * 10000
        offset = int(''.join(map(str, signal[:7])))

    output = reverse_sum(signal[offset:])
    print(''.join(map(str, output[:8])))


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
