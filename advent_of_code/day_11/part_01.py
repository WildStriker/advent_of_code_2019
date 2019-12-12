"""Part 1 Module"""
import click

from day_11.painter import count_painted


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_11.txt")
@click.option("--memory", type=int, default=2048)
def part_01(input_path, memory):
    """Part 1"""
    with open(input_path) as file_input:
        codes = list(map(int, file_input.read().split(",")))
        initial_size = len(codes)
        for _ in range(memory - initial_size):
            codes.append(0)

    count = count_painted(codes)
    print(count)


if __name__ == "__main__":
    part_01()  # pylint: disable=no-value-for-parameter
