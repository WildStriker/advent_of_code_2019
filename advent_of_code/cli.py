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
from day_09.commands import day_09
from day_10.commands import day_10
from day_11.commands import day_11
from day_12.commands import day_12
from day_13.commands import day_13
from day_14.commands import day_14
from day_15.commands import day_15
from day_16.commands import day_16
from day_17.commands import day_17
from day_18.commands import day_18
from day_19.commands import day_19
from day_20.commands import day_20


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
cli.add_command(day_09)
cli.add_command(day_10)
cli.add_command(day_11)
cli.add_command(day_12)
cli.add_command(day_13)
cli.add_command(day_14)
cli.add_command(day_15)
cli.add_command(day_16)
cli.add_command(day_17)
cli.add_command(day_18)
cli.add_command(day_19)
cli.add_command(day_20)
