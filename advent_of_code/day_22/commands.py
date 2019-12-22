"""day 22 group set up"""
import click

from day_22.part_01 import part_01
from day_22.part_02 import part_02


@click.group()
def day_22():
    """Day 22: Slam Shuffle"""


# add individual parts
day_22.add_command(part_01)
day_22.add_command(part_02)
