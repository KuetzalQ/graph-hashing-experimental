# Implementing the method of this paper: https://link.springer.com/chapter/10.1007/978-981-15-5341-7_25
import networkx as nx
import GraphUtils
import HashUtils
import matplotlib.pyplot as plt
from random import shuffle, choice, random

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

n = 250

edge_diff = []
jacc_sim = []

for i in range(0, n, 5):
    total_sim = 0
    for k in range(10):
        g = nx.gnm_random_graph(500,250)
        shingles = shingle(g)
        signature = HashUtils.minhash(set(shingles), num_hashes=400)

        h = g.copy()
        GraphUtils.randomise_labels(h)

        for j in range(i):
            GraphUtils.remove_random_edge(h)
                

        shingles2 = shingle(h)
        signature2 = HashUtils.minhash(set(shingles2), num_hashes=400)   

        minhash_sim = HashUtils.minhash_jaccard_similarity(signature, signature2, num_hashes=400)
        # edit_dist = nx.graph_edit_distance(g, h, timeout=0.5)
        print(f"{i} edge diff edit Distance: {i}, MinHash Jaccard Similarity: {minhash_sim}")

        # total_sim += minhash_sim
        edge_diff.append(i)
        jacc_sim.append(minhash_sim)

plt.scatter(edge_diff, jacc_sim, label="LSH Hashing",  marker='x')
plt.xlabel('No of edges removed')
plt.ylabel('Jaccard Similarity')   
plt.title('No of edges removed vs Jaccard Similarity predicted')
plt.grid(True)
plt.legend()
plt.show()

# Graph base size of 100 nodes, 50 edges