# Implementing the method of this paper: https://link.springer.com/chapter/10.1007/978-981-15-5341-7_25
import networkx as nx
import GraphUtils
import HashUtils
from random import shuffle, choice
import matplotlib.pyplot as plt
import time
import igraph as ig

pedge = 0.80

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

def gen_graphs(n):
    graphs = []

    for i in range(n):
        # g = nx.random_regular_graph(n = n, d = int(n / 4))
        g = nx.gnp_random_graph(no_v, pedge)
        g.name = f"graph_{i}"
        graphs.append(g.copy())
        
    original = choice(graphs)
    duplicate = GraphUtils.randomise_labels(original)
    graphs.append(duplicate.copy())  # add a relabelled, duplicated graph
    duplicate = GraphUtils.randomise_labels(original)
    graphs.append(duplicate.copy())  # add a relabelled, duplicated graph

    shuffle(graphs)
    return graphs

test_v_size = [100, 200, 300, 400, 500, 600, 700, 800]
# test_v_size = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#  110, 120, 130, 140, 150, 160, 170, 180, 190, 200
average_time = []
average_time_wf = []
false_pos = []
false_pos_wf = []

for no_v in test_v_size:
    print("Generating Graphs: ")
    graphs = gen_graphs(100)
    print("Performing on " + str(no_v) + " vertices.")

    print("LSH Algorithm Start")
    start = time.perf_counter()
    signatures = {}
    for g in graphs:
        shingles = shingle(g)
        signature = HashUtils.minhash(set(shingles), num_hashes=8)
        if signature not in signatures:
            signatures[signature] = []
        signatures[signature].append(g)

    fps = 0
    end = time.perf_counter()
    print("LSH Algorithm End")

    average_time.append(end - start)
    print("Time: " + str(end - start))

    for sig in signatures:
        if len(signatures[sig]) > 1:
            print(f"Duplicate graphs found with signature {sig}: {[i.name for i in signatures[sig]]}")
            falsePositive = False
            base = ig.Graph.from_networkx(signatures[sig][0])
            for i in range(len(signatures[sig])):
                compare = ig.Graph.from_networkx(signatures[sig][i])
                if (base.isomorphic(compare)):
                    continue
                fps += 1
                falsePositive = True
                break
            
            if falsePositive:
                print("False positive detected!")
    false_pos.append(fps)

    print("WF Algorithm Start")
    start = time.perf_counter()
    signatures = {}
    for g in graphs:
        signature = nx.weisfeiler_lehman_graph_hash(g, iterations=3)
        if signature not in signatures:
            signatures[signature] = []
        signatures[signature].append(g)
    
    fps = 0
    end = time.perf_counter()
    print("WF Algorithm End")

    average_time_wf.append(end - start)
    print("Time: " + str(end - start))

    for sig in signatures:
        if len(signatures[sig]) > 1:
            print(f"Duplicate graphs found with signature {sig}: {[i.name for i in signatures[sig]]}")
            falsePositive = False
            base = ig.Graph.from_networkx(signatures[sig][0])
            for i in range(len(signatures[sig])):
                compare = ig.Graph.from_networkx(signatures[sig][i])
                if (base.isomorphic(compare)):
                    continue
                fps += 1
                falsePositive = True
                break
            
            if falsePositive:
                print("False positive detected!")
    false_pos_wf.append(fps)

plt.subplot(1, 2, 1)
plt.plot([x * (x - 1) / 2 * pedge for x in test_v_size], average_time, label="LSH Hashing")
plt.plot([x * (x - 1) / 2 * pedge for x in test_v_size], average_time_wf, label="WFL Hash")
plt.xlabel('|E|')
plt.ylabel('Time taken to compute 100 graph hashes')   
plt.title('Graph Size (|E|) vs time taken')
plt.grid(True)
plt.legend()


plt.subplot(1, 2, 2)
plt.plot([x * (x - 1) / 2 * pedge for x in test_v_size], false_pos, label="LSH Hashing")
plt.plot([x * (x - 1) / 2 * pedge for x in test_v_size], false_pos_wf, label="WFL Hash")
plt.xlabel('|E|')
plt.ylabel('Amount of false positives')   
plt.title('Graph Size (|E|) vs no of false positives')
plt.grid(True)
plt.legend()

plt.show()