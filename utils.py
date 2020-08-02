import networkx as nx
import matplotlib.pyplot as plt


def first(arr):
    if arr is not None and len(arr) > 0:
        return arr[0]
    return None


def nodes_chunk_by_status(nodes):
    s0 = []
    s1 = []
    s2 = []
    s3 = []
    for node in nodes:
        if node.status == 0:
            s0.append(node)
        elif node.status == 1:
            s1.append(node)
        elif node.status == 2:
            s2.append(node)
        elif node.status == 3:
            s3.append(node)
    return s0, s1, s2, s3


def plot_graph(G):
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=[40, 30], dpi=80)
    nx.draw_networkx(G, pos, node_size=200, node_color='green')
    plt.axis('off')
    plt.savefig("plots/graph_before_run.png")


def plot_graph_with_status_color(G, nodes):
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=[40, 30], dpi=80)
    greens, yellows, reds, grays = nodes_chunk_by_status(nodes)
    # nodes
    nx.draw_networkx_nodes(G, pos,
                           nodelist=[node.id for node in greens],
                           node_color='green',
                           node_size=100,
                           alpha=0.8)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=[node.id for node in yellows],
                           node_color='yellow',
                           node_size=100,
                           alpha=0.8)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=[node.id for node in reds],
                           node_color='red',
                           node_size=100,
                           alpha=0.8)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=[node.id for node in grays],
                           node_color='grey',
                           node_size=100,
                           alpha=0.8)
    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    plt.axis('off')
    plt.savefig("plots/graph_after_run.png")
