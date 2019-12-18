"""day 17 group set up"""
import click

from day_17.part_01 import part_01
from day_17.part_02 import part_02


@click.group()
def day_17():
    """Day 17: Set and Forget"""


# add individual parts
day_17.add_command(part_01)
day_17.add_command(part_02)
