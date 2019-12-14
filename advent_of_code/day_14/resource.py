"""fuel resource logic"""
import collections
import math
from dataclasses import dataclass, field
from typing import Dict, TextIO

FUEL = "FUEL"
ORE = "ORE"


@dataclass
class Resource:
    """resource object output amount and related ingredients to produce"""
    name: str
    amount: int = None
    ingredients: dict = field(default_factory=dict)


def count_ore(resource_map: Dict[str, Resource], fuel: int = 1) -> int:
    """calculates the total required ORE to produce x amount of fuel

    Arguments:
        resource_map {Dict[str, Resource]} -- resource map of all production outputs

    Keyword Arguments:
        fuel {int} -- fuel requried (default: {1})

    Returns:
        int -- ore resource to create fuel required
    """
    # init require resources, we know we at least need fuel
    required = collections.defaultdict(int)
    required[FUEL] = fuel

    # resource queue management, we want to find minimum require ore
    queue = [resource_map[FUEL]]
    while queue:
        resource = queue.pop()

        # round up to the lowest required resource needed
        need = math.ceil(required[resource.name] / resource.amount)

        # all ingredients need to be expanded to match our resource needs
        for ingredient, amount in resource.ingredients.items():
            required[ingredient] += need * amount

            # ORE has no other components so do not add to queue
            if ingredient != ORE:
                queue.append(resource_map[ingredient])

        # negative = left over amounts, can \ will be reused
        required[resource.name] -= need * resource.amount

    return required[ORE]


def count_fuel(resource_map: Dict[str, Resource], ore: int) -> int:
    """perform a binary search to find total fuel output

    Arguments:
        resource_map {Dict[str, Resource]} -- resource map
        ore {int} -- total amount of raw ORE we want to use

    Returns:
        int -- fuel output
    """
    # get our range, total fuel is somewhere here
    low_fuel = ore // count_ore(resource_map)
    high_fuel = low_fuel * 2

    while high_fuel > low_fuel:

        # pivot point
        mid_fuel = (high_fuel + low_fuel) // 2

        if mid_fuel == low_fuel:
            break

        ore_required = count_ore(resource_map, mid_fuel)

        # if too much ore is used, mid is now high
        # otherwise low
        if ore_required > ore:
            high_fuel = mid_fuel
        else:
            low_fuel = mid_fuel

    return low_fuel


def parse_input(file_input: TextIO) -> Dict[str, Resource]:
    """parse resource map

    Arguments:
        file_input {TextIO} -- file stream

    Returns:
        Dict[str, Resource] -- resource production mapped
    """

    resource_map = {}
    for line in file_input:
        ingredients, resource = line.strip().split(" => ")
        ingredients = ingredients.split(", ")

        amount, resource = resource.split(" ")
        amount = int(amount)
        resource: Resource = resource_map.setdefault(
            resource, Resource(resource))
        resource.amount = amount

        for ingredient in ingredients:
            amount, ingredient = ingredient.split(" ")
            amount = int(amount)
            resource.ingredients[ingredient] = amount

    return resource_map
