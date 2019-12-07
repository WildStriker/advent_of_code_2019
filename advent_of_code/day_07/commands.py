"""day 07 group set up"""
import click

from day_07.part_01 import part_01
from day_07.part_02 import part_02


@click.group()
def day_07():
    """Day 7: Amplification Circuit"""


# add individual parts
day_07.add_command(part_01)
day_07.add_command(part_02)
