"""day 11 group set up"""
import click

from day_11.part_01 import part_01
from day_11.part_02 import part_02


@click.group()
def day_11():
    """Day 11: Space Police"""


# add individual parts
day_11.add_command(part_01)
day_11.add_command(part_02)
