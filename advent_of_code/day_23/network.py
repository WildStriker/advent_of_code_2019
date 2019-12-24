"""network logic"""
import concurrent.futures
import copy
import queue
import time
from dataclasses import dataclass, field
from typing import DefaultDict

from shared.opcodes import process


class NetworkHalt(Exception):
    """Exception raised when network loop stops"""


@dataclass
class NATQueue:
    """NAT Queue, only holds last given value"""
    queue: tuple = None

    def put(self, value):
        """replace value in queue"""
        self.queue = value


@dataclass
class NAT:
    """NAT montiors the network
    when network is completely idle it will restart it by
    sending value to address 0 queue"""
    address: int
    network: dict
    is_running: bool = True
    packets: NATQueue = field(default_factory=NATQueue)
    last_sent: tuple = None

    def run(self):
        """NAT network loop, monitor for inactivity"""
        delay = 0.001
        while not self.packets.queue:
            time.sleep(delay)

        while True:
            time.sleep(delay)
            is_idle = True
            for address in self.network:
                network_manager = self.network[address]

                # not monitoring self
                if address == self.address:
                    continue

                # flag all machines as idle
                # if there is any output it will undo this
                if not network_manager.is_idle:
                    network_manager.is_idle = True
                    is_idle = False

            if is_idle:
                if self.last_sent and self.packets.queue[1] == self.last_sent[1]:
                    return self.address, self.last_sent[0], self.last_sent[1]
                else:
                    self.network[0].packets.put(self.packets.queue)
                    self.last_sent = self.packets.queue
                    time.sleep(delay)


@dataclass
class NetworkManger:
    """manages machines output and inputs
    on the network"""
    address: int
    codes: DefaultDict
    network: dict
    # FIFO queue
    packets: queue.Queue = field(default_factory=queue.Queue)
    y_portion: int = None

    is_running = True
    is_idle = False

    _address_set: bool = False

    def packet_input(self):
        """inputs for intcode machine"""

        # stop if not running
        if not self.is_running:
            raise NetworkHalt

        # set network address
        if not self._address_set:
            self._address_set = True
            return self.address

        # send y of last packet
        if self.y_portion:
            y_portion = self.y_portion
            self.y_portion = None
            return y_portion

        try:
            x_portion, y_poriton = self.packets.get(timeout=0.001)
            # save y for later
            self.y_portion = y_poriton
            # send x
            return x_portion
        except queue.Empty:
            # nothing in queue
            return -1

    def run(self):
        """network loop, when output exists
        send to existing machine on the network"""
        try:
            machine = process(copy.copy(self.codes), self.packet_input)
            while True:
                address = next(machine)
                x_portion = next(machine)
                y_portion = next(machine)
                self.is_idle = False

                # unknown network address
                if address not in self.network:
                    return address, x_portion, y_portion

                # queue output to proper machine
                network_manager = self.network[address]
                # recieved input, not idle
                network_manager.is_idle = False
                network_manager.packets.put((x_portion, y_portion))

        except NetworkHalt:
            pass


def communicate(codes: DefaultDict[int, int], machine_count=50, nat_address=None) -> int:
    """start network communication

    Arguments:
        codes {DefaultDict[int, int]} -- intcode machine instructions

    Keyword Arguments:
        machine_count {int} -- total machine count on network (default: {50})
        nat_address {[type]} -- if included there will "nat" monitoring the network

    Returns:
        int -- returns address, x, y if address out of range (255) or nat detected repeated inputs
    """
    network = {}

    if nat_address:
        nat = NAT(nat_address, network)
        network[nat_address] = nat
        machine_count += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=machine_count) as executor:
        futures = {}
        for address in range(machine_count):
            network_manager = NetworkManger(address, codes, network)
            network[address] = network_manager

        for address, network_manager in network.items():
            future = executor.submit(network_manager.run)
            futures[future] = address

        for future in concurrent.futures.as_completed(futures):
            for network_manager in network.values():
                network_manager.is_running = False

            return future.result()
