"""day 16 group set up"""
import click

from day_16.part_01 import part_01
from day_16.part_02 import part_02


@click.group()
def day_16():
    """Day 16: Flawed Frequency Transmission"""


# add individual parts
day_16.add_command(part_01)
day_16.add_command(part_02)
