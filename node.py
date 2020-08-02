import numpy as np
import threading
import time
import random
import utils
import settings
import os


class Node(threading.Thread):

    def __init__(self, index, status=0, debug=True):
        super().__init__()
        self.debug = debug
        # When this flag is set, the node will stop and close (dead)
        self.terminate_flag = threading.Event()

        self.id = index
        self.status = status
        self.neighbors = []  # Nodes that are close connected to the node
        self.p = 0
        self.q = 0
        self.r0 = 0
        self.infection_start_time = 0
        self.infection_end_time = 0
        "Max period of having disease, after this time, node must be recovered or dead"
        self.t = int(os.getenv("T"))

    def debug_print(self, message):
        """When the debug flag is set to True, all debug messages are printed in the console."""
        if self.debug:
            print("\nDEBUG: " + message)

    def infect(self, victom_node):
        if not victom_node.terminate_flag.is_set() and victom_node.is_alive() and self.r0 > 1 - self.r0\
                and victom_node.infection_start_time == 0 and \
                victom_node.infection_end_time == 0:
            victom_node.status = 1
            victom_node.infection_start_time = time.time()
            victom_node.p = np.random.random()
            victom_node.q = 1 - victom_node.p
            victom_node.r0 = np.random.random()
            self.debug_print("Node: " + str(victom_node.id) + " infected by Node: " + str(self.id))

    def get_sample_of_neighbors(self, status=0, size=1):
        selected_neighbors = []
        for neighbor in self.neighbors:
            if neighbor.status == status and not neighbor.terminate_flag.is_set()\
                    and neighbor.is_alive():
                selected_neighbors.append(neighbor)
        if len(selected_neighbors) > 0:
            return random.sample(selected_neighbors, size)
        return None

    def recover_or_die(self):
        self.infection_end_time = time.time()
        if self.p > self.q:
            self.status = 3
            self.debug_print("Node:" + str(self.id) + " is recovered")
        else:
            self.debug_print("Node:" + str(self.id) + " is dead")
            self.die()

    def die(self):
        """Stop this node"""
        self.terminate_flag.set()

    def stop(self):
        """Stop this node"""
        self.terminate_flag.set()

    def run(self):
        """The main loop of the thread that deals with connections from other nodes on the network."""
        self.debug_print("Node:" + str(self.id) + " started.")
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            try:
                if self.status == 1 or self.status == 2:
                    victom = utils.first(self.get_sample_of_neighbors(status=0, size=1))
                    if victom is not None:
                        self.infect(victom)
                    infection_time = time.time() - self.infection_start_time
                    if infection_time >= self.t:
                        self.recover_or_die()

            except Exception as e:
                raise e
        self.debug_print("Node:" + str(self.id) + " stopped.")
