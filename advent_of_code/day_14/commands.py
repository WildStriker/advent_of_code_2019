"""day 14 group set up"""
import click

from day_14.part_01 import part_01
from day_14.part_02 import part_02


@click.group()
def day_14():
    """Day 14: Space Stoichiometry"""


# add individual parts
day_14.add_command(part_01)
day_14.add_command(part_02)
