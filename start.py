from node import Node
import numpy as np
import random
import time
import utils
import settings
import os
import sys
# import pygraphviz as pgv
import networkx as nx
import matplotlib.pyplot as plt

node_status_dict = {0: "green", 1: "yellow", 2: "red", 3: "gray"}

print("Starting..")

"""The n is the number of node in the graph."""
n = int(os.getenv("Nodes_Count"))
nodes = [Node(i + 1, debug=True) for i in range(0, n)]
nodes_edges = np.random.randint(0, 2, (n, n))

"""Generating random graph.."""
graph = nx.Graph()
for node in nodes:
    graph.add_node(node.id, obj=node)

row = 0
for node_edge in nodes_edges:
    node = nodes[row]
    col = 0
    edge_chance = random.randint(0, 100)
    for edge in node_edge:
        if edge == 1 and row != col and edge_chance > 50:
            neighbor = nodes[col]
            graph.add_edge(node.id, neighbor.id)
        col += 1
    row += 1

"""Plot network graph before disease spread"""
utils.plot_graph(graph)

"""Infect one random victom node"""
infectious_node = utils.first(random.sample(nodes, 1))
if infectious_node is not None:
    infectious_node.status = 1
    infectious_node.infection_start_time = 0
    infectious_node.p = np.random.random()
    infectious_node.q = 1 - infectious_node.p
    infectious_node.r0 = np.random.random()
    print("Victom Node: " + str(infectious_node.id) + " infected.")

print("Starting network..")
"""calling run method foreach node thread"""
for node in nodes:
    node.start()

"""running network seconds"""
time.sleep(int(os.getenv("NETWORK_RUN_TIME")))

for node in nodes:
    node.stop()

for node in nodes:
    node.join()
print("Network stopped.")

"""Plot network graph with colors according to nodes status"""
utils.plot_graph_with_status_color(graph, nodes)
