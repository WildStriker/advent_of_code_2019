"""shared module for day 01"""


def calc_fuel(mass):
    """calculate the required fuel given mass"""
    fuel = mass // 3 - 2
    if fuel < 0:
        return 0
    return fuel
