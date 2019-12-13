"""moon orbit logic"""
import itertools
import math
import re
from dataclasses import dataclass
from typing import List, TextIO


@dataclass
class Moon:
    """hold current position and velocity of a moon"""
    position: List[int]
    velocity: List[int]


def parse_input(file_input: TextIO) -> List[Moon]:
    """parse file stream to generate list of moon objects

    Arguments:
        file_input {TextIO} -- text stream

    Raises:
        ValueError: unexpected line read

    Returns:
        List[Moon] -- list of moons from input
    """
    pattern = re.compile("<x=(.*), y=(.*), z=(.*)>")

    moons = []
    for line in file_input:
        result = pattern.match(line)
        if not result:
            raise ValueError("Unexpected input")
        position = list(map(int, result.groups())
                        )  # pylint: disable=invalid-name
        velocity = [0, 0, 0]
        moons.append(Moon(position, velocity))

    return moons


def gravity_axis(moons: List[Moon], index):
    """apply gravity to one axis, this will increase current velocity

    Arguments:
        moons {List[Moon]} -- list of moons
        index {[type]} -- current axis
    """
    combos = itertools.combinations(moons, 2)
    for moon1, moon2 in combos:
        if moon1.position[index] == moon2.position[index]:
            pass
        elif moon1.position[index] < moon2.position[index]:
            moon1.velocity[index] += 1
            moon2.velocity[index] -= 1
        elif moon1.position[index] > moon2.position[index]:
            moon1.velocity[index] -= 1
            moon2.velocity[index] += 1


def apply_gravity(moons: List[Moon]):
    """apply gravity to all axis

    Arguments:
        moons {List[Moon]} -- list of moons
    """
    for index in range(len(moons[0].position)):
        gravity_axis(moons, index)


def apply_velocity(moons: List[Moon]):
    """applies velocity to the moon's position

    Arguments:
        moons {List[Moon]} -- list of moons
    """
    for moon in moons:
        for index in range(len(moon.position)):
            moon.position[index] += moon.velocity[index]


def calc_energy(moons: List[Moon], total_steps: int):
    """calculate total enegry at a given step

    Arguments:
        moons {List[Moon]} -- list of moons
        total_steps {int} -- target step count
    """
    for _ in range(total_steps):
        apply_gravity(moons)

        apply_velocity(moons)

    print(f"After {total_steps} steps:")
    for moon in moons:
        print(moon)

    total_energy = 0
    for moon in moons:
        potential = 0
        kinetic = 0
        for index in range(len(moon.position)):
            potential += abs(moon.position[index])
            kinetic += abs(moon.velocity[index])
        total_energy += potential * kinetic

    print(total_energy)


def find_repeat(moons: List[Moon]) -> int:
    """find a repeated values i both position and velocity

    Arguments:
        moons {List[Moon]} -- list of moons

    Returns:
        int -- total steps taken to get to a repeated position
    """
    axis_steps = []

    axis = len(moons[0].position)
    for index in range(axis):

        occurence = []
        for moon in moons:
            occurence.append(moon.position[index])
            occurence.append(moon.velocity[index])
        first_ocurrence = tuple(occurence)

        steps = 0

        while True:
            occurence = []
            steps += 1

            # apply gravity to this axis
            gravity_axis(moons, index)

            # apply velocity and track occurence
            for moon in moons:
                moon.position[index] += moon.velocity[index]
                occurence.append(moon.position[index])
                occurence.append(moon.velocity[index])
            occurence = tuple(occurence)
            if occurence == first_ocurrence:
                break
        axis_steps.append(steps)

    total_steps = axis_steps[0]
    for step in axis_steps:
        total_steps = total_steps * step // math.gcd(total_steps, step)

    return total_steps
