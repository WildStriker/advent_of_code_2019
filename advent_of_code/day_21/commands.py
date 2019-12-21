"""day 21 group set up"""
import click

from day_21.part_01 import part_01
from day_21.part_02 import part_02


@click.group()
def day_21():
    """Day 21: Springdroid Adventure"""


# add individual parts
day_21.add_command(part_01)
day_21.add_command(part_02)
