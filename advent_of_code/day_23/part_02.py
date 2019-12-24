"""Part 2 Module"""
import click

from day_23.network import communicate
from shared.opcodes import read_codes


@click.command()
@click.option("--input", "input_path", type=click.Path(exists=True), default="inputs\\day_23.txt")
def part_02(input_path):
    """Part 2"""
    with open(input_path) as file_input:
        codes = read_codes(file_input)

    nat_address = 255
    address, x_portion, y_portion = communicate(codes, nat_address=nat_address)

    if address != nat_address:
        print(f"{address} is outside address range")
        print(f"Tried to send packet x: {x_portion} and y: {y_portion}")
    else:
        print(f"NAT address has sent y twice: {y_portion}")


if __name__ == "__main__":
    part_02()  # pylint: disable=no-value-for-parameter
