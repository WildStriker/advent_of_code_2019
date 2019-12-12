"""Part 2 Module"""
import click

from day_11.painter import WHITE, render_painted


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_11.txt")
@click.option("--memory", type=int, default=1024)
def part_02(input_path, memory):
    """Part 2"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))
        initial_size = len(codes)
        for _ in range(memory - initial_size):
            codes.append(0)

    render_painted(codes, {(0, 0): WHITE})


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
