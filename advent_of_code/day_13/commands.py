"""day 13 group set up"""
import click

from day_13.part_01 import part_01
from day_13.part_02 import part_02


@click.group()
def day_13():
    """Day 13: Care Package"""


# add individual parts
day_13.add_command(part_01)
day_13.add_command(part_02)
