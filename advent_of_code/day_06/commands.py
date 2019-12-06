"""day 06 group set up"""
import click

from day_06.part_01 import part_01
from day_06.part_02 import part_02


@click.group()
def day_06():
    """Day 6: Universal Orbit Map"""


# add individual parts
day_06.add_command(part_01)
day_06.add_command(part_02)
