"""orbit logic module"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ObjectMass:
    """Keep track of ObjectMass orbit / orbitters"""
    name: str
    orbit: 'ObjectMass' = None
    orbiters: List['ObjectMass'] = field(default_factory=list)

    def orbit_count(self) -> int:
        """counts total number of objects this object is orbitings (directly and indirectly)

        Returns:
            int -- total orbit count
        """
        if self.orbit:
            return 1 + self.orbit.orbit_count()
        return 0

    def get_orbit_hops(self) -> Dict[str, int]:
        """return a dict with total "hop" count to each orbit

        Returns:
            Dict[str, int] -- key value pair of mass name and its "hop" distance
        """
        total = 0
        orbit_hops = {}

        orbit = self.orbit

        while orbit:
            orbit_hops[orbit.name] = total
            orbit = orbit.orbit
            total += 1

        return orbit_hops


def init_objects(file_input: str) -> Dict[str, ObjectMass]:
    """parse inputs to create a list of ObjectMass

    init any relationships based on the mapping

    Arguments:
        file_input {str} -- file stream with relation mapping

    Returns:
        Dict[str, ObjectMass] -- object representation of inputs
    """
    objects = {}
    for line in file_input:
        orbit, orbiter = line.strip().split(")")

        orbit: ObjectMass = objects.setdefault(orbit, ObjectMass(orbit))
        orbiter: ObjectMass = objects.setdefault(orbiter, ObjectMass(orbiter))

        orbit.orbiters.append(orbiter)
        orbiter.orbit = orbit

    return objects


def orbit_count(objects: Dict[str, ObjectMass]) -> int:
    """loop through each object and get total orbit counts

    Arguments:
        objects {Dict[str, ObjectMass]} -- count list we are looping through

    Returns:
        int -- total direct and indirect orbits
    """
    total = 0

    for mass in objects.values():
        total += mass.orbit_count()

    return total


def distance(mass_1: ObjectMass, mass_2: ObjectMass) -> int:
    """calculate the total orbits between these two masses

    Arguments:
        mass_1 {ObjectMass} -- first mass
        mass_2 {ObjectMass} -- second mass

    Returns:
        int -- total orbit "distance"
    """

    # collect orbit hops
    orbits_1 = mass_1.get_orbit_hops()

    orbits_2 = mass_2.get_orbit_hops()

    # find common orbit hop with least amount of hops
    common_hops: set = orbits_1.keys() & orbits_2.keys()

    hop = common_hops.pop()
    smallest_total_hops = orbits_1[hop] + orbits_2[hop]
    for hop in common_hops:
        total_hops = orbits_1[hop] + orbits_2[hop]

        if total_hops < smallest_total_hops:
            smallest_total_hops = total_hops

    return smallest_total_hops
