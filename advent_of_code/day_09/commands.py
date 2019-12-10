"""day 09 group set up"""
import click

from day_09.part_01 import part_01
from day_09.part_02 import part_02


@click.group()
def day_09():
    """Day 9: Sensor Boost"""


# add individual parts
day_09.add_command(part_01)
day_09.add_command(part_02)
