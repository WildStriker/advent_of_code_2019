"""day 24 group set up"""
import click

from day_24.part_01 import part_01
from day_24.part_02 import part_02


@click.group()
def day_24():
    """Day 24: Planet of Discord"""


# add individual parts
day_24.add_command(part_01)
day_24.add_command(part_02)
