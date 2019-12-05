"""day 04 group set up"""
import click

from day_04.part_01 import part_01
from day_04.part_02 import part_02


@click.group()
def day_04():
    """Day 4: Secure Container"""


# add individual parts
day_04.add_command(part_01)
day_04.add_command(part_02)
