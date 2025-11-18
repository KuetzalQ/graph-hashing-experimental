# https://github.com/TrustAGI-Lab/graph_datasets
from random import choice, shuffle
import networkx as nx

def add_random_edge(g: nx.Graph) -> None:
    nonedges = list(nx.non_edges(g))
    edge = choice(nonedges)
    g.add_edge(edge[0], edge[1])


def remove_random_edge(g: nx.Graph) -> None:
    edges = list(nx.edges(g))
    edge = choice(edges)
    g.remove_edge(edge[0], edge[1])

def randomise_labels(g: nx.Graph) -> nx.Graph:
    nodes = list(g.nodes)
    copied = nodes.copy()
    shuffle(copied)
    relabelled = nx.relabel_nodes(g, dict(zip(nodes, copied)), copy=True)
    h = nx.Graph()
    h.add_nodes_from(sorted(relabelled.nodes()))
    h.add_edges_from(relabelled.edges())
    h.name = g.name + "_relabelled"
    return h

