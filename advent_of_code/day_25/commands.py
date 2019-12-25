"""day 25 group set up"""
import click

from day_25.part_01 import part_01


@click.group()
def day_25():
    """Day 25: Cryostasis"""


# add individual parts
day_25.add_command(part_01)
