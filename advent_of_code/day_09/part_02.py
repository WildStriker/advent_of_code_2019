"""Part 2 Module"""
import click

from day_09.boost import run


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_09.txt")
@click.option("--phase", type=int, default=2)
@click.option("--memory", type=int, default=2048)
def part_02(input_path, phase, memory):
    """Part 2"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))
        initial_size = len(codes)
        for _ in range(memory - initial_size):
            codes.append(0)

    run(codes, phase)


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter