# Implementing the method of this paper: https://link.springer.com/chapter/10.1007/978-981-15-5341-7_25
import networkx as nx
import GraphUtils
import HashUtils
from random import shuffle, choice

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
n = 1000

for i in range(n):
    g = nx.gnm_random_graph(200,100)
    g.name = f"graph_{i}"
    graphs.append(g.copy())
    
original = choice(graphs)
duplicate = GraphUtils.randomise_labels(original)
graphs.append(duplicate.copy())  # add a relabelled, duplicated graph
shuffle(graphs)

signatures = {}
for g in graphs:
    shingles = shingle(g)
    signature = HashUtils.minhash(set(shingles), num_hashes=64)
    if signature not in signatures:
        signatures[signature] = []
    signatures[signature].append(g)

fps = 0
for sig in signatures:
    if len(signatures[sig]) > 1:
        print(f"Duplicate graphs found with signature {sig}: {[i.name for i in signatures[sig]]}")
        falsePositive = False
        for i in range(len(signatures[sig])-1):
            if nx.is_isomorphic(signatures[sig][i], signatures[sig][i+1]):
                continue
            falsePositive = True
        if falsePositive:
            fps += 1
            print("False positive detected!")

print(fps)