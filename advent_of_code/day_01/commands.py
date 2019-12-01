"""day 01 group set up"""
import click

from day_01.part_01 import part_01
from day_01.part_02 import part_02


@click.group()
def day_01():
    """Day 1: The Tyranny of the Rocket Equation"""


# add individual parts
day_01.add_command(part_01)
day_01.add_command(part_02)
