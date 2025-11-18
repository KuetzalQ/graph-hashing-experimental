# Implementing the method of this paper: https://link.springer.com/chapter/10.1007/978-981-15-5341-7_25
import networkx as nx
import matplotlib.pyplot as plt
from Dataset import sample1
import GraphUtils

def shingle(g: nx.Graph):
    nodes = list(g.nodes())
    shingles = []
    for node in nodes:
        shingle = []
        for neighbour in g.neighbors(node):
            shingle.append(g.degree(neighbour))
        shingles.append(tuple(sorted(shingle)))
    # doesn't matter whether shingles are sorted or not
    return shingles

def minhash(shingles, length=10):
    pass

graphs = []
# for i in range()
all = set()

for i in range(50):
    g = nx.gnm_random_graph(20,10)
    shingles = shingle(g)
    for i in shingles: all.add(i)

print(len(all))