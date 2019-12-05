"""main cli group, hook up all days here"""
import click

from day_01.commands import day_01
from day_02.commands import day_02
from day_03.commands import day_03
from day_04.commands import day_04


@click.group()
def cli():
    """Advent of Code 2019"""


# add days commands to main cli group
cli.add_command(day_01)
cli.add_command(day_02)
cli.add_command(day_03)
cli.add_command(day_04)
