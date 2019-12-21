"""day 20 group set up"""
import click

from day_20.part_01 import part_01
from day_20.part_02 import part_02


@click.group()
def day_20():
    """Day 20: Donut Maze"""


# add individual parts
day_20.add_command(part_01)
day_20.add_command(part_02)
