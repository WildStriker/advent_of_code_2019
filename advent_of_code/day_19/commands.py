"""day 19 group set up"""
import click

from day_19.part_01 import part_01
from day_19.part_02 import part_02


@click.group()
def day_19():
    """Day 19: Tractor Beam"""


# add individual parts
day_19.add_command(part_01)
day_19.add_command(part_02)
