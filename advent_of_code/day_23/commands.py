"""day 23 group set up"""
import click

from day_23.part_01 import part_01
from day_23.part_02 import part_02


@click.group()
def day_23():
    """Day 23: Category Six"""


# add individual parts
day_23.add_command(part_01)
day_23.add_command(part_02)
