"""day 10 group set up"""
import click

from day_10.part_01 import part_01
from day_10.part_02 import part_02


@click.group()
def day_10():
    """Day 10: Monitoring Station"""


# add individual parts
day_10.add_command(part_01)
day_10.add_command(part_02)
