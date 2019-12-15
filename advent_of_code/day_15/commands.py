"""day 15 group set up"""
import click

from day_15.part_01 import part_01
from day_15.part_02 import part_02


@click.group()
def day_15():
    """Day 15: Oxygen System"""


# add individual parts
day_15.add_command(part_01)
day_15.add_command(part_02)
