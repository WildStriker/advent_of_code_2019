"""repair bot logic module"""
import copy
import queue
from typing import DefaultDict, List

from shared.opcodes import process

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

FAILED = 0  # Wall present
SUCCESS = 1  # Droid Moved
OXY_SYSTEM = 2  # Found Oxygen System

class Droid:
    """Droid state, init mapping and find oxygen system"""

    def __init__(self, codes):
        # init droid position and frontier
        self.position = (0, 0)

        # mark as unpassable (wall)
        self.unpassable = set()

        self.passable = {self.position}

        # target positions to look for
        self.check = self.get_neighbors(*self.position)

        self.next = None
        self.route = None

        self.codes = codes
        self.state = None

        self.oxy_location = None

    def init_map(self):
        """initialize the map state by traversing to the furthest unknown area"""
        self.state = process(copy.copy(self.codes), self._blind_input)
        self._run()

    def _run(self):
        for output in self.state:
            # there is a wall here
            if output == FAILED:
                self.unpassable.add(self.next)

                # remove from check
                if self.next == self.check[-1]:
                    self.check.pop()

                # clear route, not valid
                self.route = None
            # movable!
            elif output == SUCCESS:
                self.position = self.next
                self.passable.add(self.position)
            # system found!
            elif output == OXY_SYSTEM:
                self.position = self.next
                self.oxy_location = self.next

            # found last target, clear it off list
            if self.check and self.position == self.check[-1]:
                self.check.pop()

                neighbors = self.get_neighbors(*self.position)
                for neighbor in neighbors:
                    if neighbor not in self.unpassable and neighbor not in self.passable:
                        self.check.append(neighbor)

                self.route = None

            # all squares checked
            if not self.check:
                return

    def find_path(self):
        """once map is initialized we can determine the shortest path to the oxygen system"""
        # get path
        self.position = (0, 0)
        self.next = None
        path = self.dijkstra(self.position, self.oxy_location)

        return len(path)

    def _blind_input(self) -> int:
        """helper function to provide input to state intcode machine"

        Returns:
            int -- directional input
        """
        target = self.check[-1]
        if not self.route:
            self.route = self.dijkstra(self.position, target)

        # pop off route and feed to state
        self.next = self.route.pop()
        return self.direction()

    def direction(self) -> int:
        """expected directional inputs for state

        Returns:
            int -- directional input
        """
        if self.position[0] > self.next[0]:
            return NORTH

        if self.position[0] < self.next[0]:
            return SOUTH

        if self.position[1] > self.next[1]:
            return WEST

        if self.position[1] < self.next[1]:
            return EAST

    def get_neighbors(self, y_pos: int, x_pos: int) -> List[tuple]:
        """get neighboring coordinators to a given position

        Arguments:
            y_pos {int} -- given y position
            x_pos {int} -- given x position

        Returns:
            List[tuple] -- 4 neighboring coordinates
        """
        neighbors = []
        # up
        up_coord = (y_pos-1, x_pos)
        neighbors.append(up_coord)

        # left
        left_coord = (y_pos, x_pos - 1)
        neighbors.append(left_coord)

        # right
        right_coord = (y_pos, x_pos + 1)
        neighbors.append(right_coord)

        # down
        down_coord = (y_pos+1, x_pos)
        neighbors.append(down_coord)

        return neighbors

    def dijkstra(self, start: tuple, goal: tuple) -> List[tuple]:
        """dijkstra algorithm, lists a path given starting and ending coordinates

        Arguments:
            start {tuple} -- starting location
            goal {tuple} -- ending location

        Returns:
            List[tuple] -- list of coordinates (reversed order)
        """
        frontier = queue.PriorityQueue()
        frontier.put((0, start))

        came_from = {
            start: None
        }
        cost_so_far = {
            start: 0
        }

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            neighbors = []
            for neighbor in self.get_neighbors(*current):
                if neighbor == goal:
                    neighbors = [goal]
                    break
                elif neighbor not in self.unpassable:
                    neighbors.append(neighbor)

            weight = 1
            for neighbor in neighbors:
                new_cost = cost_so_far[current] + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    frontier.put((priority, neighbor))
                    came_from[neighbor] = current

        if goal not in came_from:
            return None

        path = []
        current_path = came_from[goal]
        path.append(goal)
        while current_path != start:
            path.append(current_path)
            current_path = came_from[current_path]
        return path

    def fill_oxy(self) -> int:
        """fill all areas with oxygen, calculate total time that passes

        Returns:
            int -- minutes passed until all areas have oxygen
        """
        minutes = 0
        filling = [self.oxy_location]
        next_area = []
        has_oxy = set(filling)
        while self.passable - has_oxy:
            while filling:
                current = filling.pop()
                neighbors = self.get_neighbors(*current)
                for neighbor in neighbors:
                    if neighbor not in self.unpassable and neighbor not in has_oxy:
                        has_oxy.add(neighbor)
                        next_area.append(neighbor)
            filling = next_area
            next_area = []
            minutes += 1
        return minutes


def count_steps(codes: DefaultDict[int, int]) -> int:
    """count shortests path to oxygen system given instructions

    Arguments:
        codes {DefaultDict[int, int]} -- intcode instructions

    Returns:
        int -- total steps taken to get to oxygen system
    """
    droid = Droid(codes)

    droid.init_map()

    length = droid.find_path()

    return length


def fill_oxygen(codes: DefaultDict[int, int]) -> int:
    """given intcode instructions to init map,
    determine how long until all areas have oxygen

    Arguments:
        codes {DefaultDict[int, int]} -- [description]

    Returns:
        int -- [description]
    """
    droid = Droid(codes)

    droid.init_map()

    minutes = droid.fill_oxy()

    return minutes
