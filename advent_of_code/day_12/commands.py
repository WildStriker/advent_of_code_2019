"""day 12 group set up"""
import click

from day_12.part_01 import part_01
from day_12.part_02 import part_02


@click.group()
def day_12():
    """Day 12: The N-Body Problem"""


# add individual parts
day_12.add_command(part_01)
day_12.add_command(part_02)
