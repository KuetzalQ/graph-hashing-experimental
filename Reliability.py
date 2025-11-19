# Implementing the method of this paper: https://link.springer.com/chapter/10.1007/978-981-15-5341-7_25
import networkx as nx
import GraphUtils
import HashUtils
from random import shuffle, choice
import matplotlib.pyplot as plt
import time
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash

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

test_v_size = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

average_time = []
false_pos = []

for no_v in test_v_size:
    graphs = []
    # Running it on 500 graphs to prevent biases in average
    n = 50

    for i in range(n):
        g = nx.gnp_random_graph(no_v, 0.6)
        # g = nx.gnm_random_graph(no_v, no_v * 100)
        g.name = f"graph_{i}"
        graphs.append(g.copy())
        
    original = choice(graphs)
    duplicate = GraphUtils.randomise_labels(original)
    graphs.append(duplicate.copy())  # add a relabelled, duplicated graph
    duplicate = GraphUtils.randomise_labels(original)
    graphs.append(duplicate.copy())  # add a relabelled, duplicated graph
    shuffle(graphs)

    start = time.perf_counter()

    signatures = {}
    for g in graphs:
        shingles = shingle(g)
        signature = HashUtils.minhash(set(shingles), num_hashes=64)
        if signature not in signatures:
            signatures[signature] = []
        signatures[signature].append(g)

    fps = 0
    end = time.perf_counter()

    average_time.append(end - start)
    print(end - start)

    for sig in signatures:
        if len(signatures[sig]) > 1:
            print(f"Duplicate graphs found with signature {sig}: {[i.name for i in signatures[sig]]}")
            falsePositive = False
            for i in range(len(signatures[sig])-1):
                if (nx.is_isomorphic(signatures[sig][i], signatures[sig][i + 1])):
                    continue
                falsePositive = True
            if falsePositive:
                fps += 1
                print("False positive detected!")
    false_pos.append(fps)

plt.subplot(2, 1, 1)
plt.plot(test_v_size, average_time)
plt.xlabel('(|V| + |E|) / 2')
plt.ylabel('Time taken to compute 1000 graph hashes')   
plt.title('Graph Size (|V| + |E|) vs time taken')
plt.grid(True)    

plt.subplot(2, 1, 2)
plt.plot(test_v_size, false_pos) 
plt.xlabel('|V|')
plt.ylabel('Number of False Positives')
plt.title('Graph no of vertices (|V|) vs False Positives (Probability of edges: 0.6)')
plt.grid(True)
plt.show()