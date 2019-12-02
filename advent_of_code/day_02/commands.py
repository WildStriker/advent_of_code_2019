"""day 02 group set up"""
import click

from day_02.part_01 import part_01
from day_02.part_02 import part_02


@click.group()
def day_02():
    """Day 2: 1202 Program Alarm"""


# add individual parts
day_02.add_command(part_01)
day_02.add_command(part_02)
