"""day 05 group set up"""
import click

from day_05.part_01 import part_01
from day_05.part_02 import part_02


@click.group()
def day_05():
    """Day 5: Sunny with a Chance of Asteroids"""


# add individual parts
day_05.add_command(part_01)
day_05.add_command(part_02)
