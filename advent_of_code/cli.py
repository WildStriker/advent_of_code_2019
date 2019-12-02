"""main cli group, hook up all days here"""
import click

from day_01.commands import day_01
from day_02.commands import day_02


@click.group()
def cli():
    """Advent of Code 2019"""


# add days commands to main cli group
cli.add_command(day_01)
cli.add_command(day_02)
