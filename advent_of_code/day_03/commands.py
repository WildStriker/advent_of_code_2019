"""day 03 group set up"""
import click

from day_03.part_01 import part_01
from day_03.part_02 import part_02


@click.group()
def day_03():
    """Day 3: Crossed Wires"""


# add individual parts
day_03.add_command(part_01)
day_03.add_command(part_02)
