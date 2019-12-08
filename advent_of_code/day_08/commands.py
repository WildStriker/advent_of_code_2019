"""day 08 group set up"""
import click

from day_08.part_01 import part_01
from day_08.part_02 import part_02


@click.group()
def day_08():
    """Day 8: Space Image Format"""


# add individual parts
day_08.add_command(part_01)
day_08.add_command(part_02)
