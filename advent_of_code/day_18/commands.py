"""day 18 group set up"""
import click

from day_18.part_01 import part_01
from day_18.part_02 import part_02


@click.group()
def day_18():
    """Day 18: Many-Worlds Interpretation"""


# add individual parts
day_18.add_command(part_01)
day_18.add_command(part_02)
