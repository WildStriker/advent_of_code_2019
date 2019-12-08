"""main cli group, hook up all days here"""
import click

from day_01.commands import day_01
from day_02.commands import day_02
from day_03.commands import day_03
from day_04.commands import day_04
from day_05.commands import day_05
from day_06.commands import day_06
from day_07.commands import day_07
from day_08.commands import day_08


@click.group()
def cli():
    """Advent of Code 2019"""


# add days commands to main cli group
cli.add_command(day_01)
cli.add_command(day_02)
cli.add_command(day_03)
cli.add_command(day_04)
cli.add_command(day_05)
cli.add_command(day_06)
cli.add_command(day_07)
cli.add_command(day_08)
