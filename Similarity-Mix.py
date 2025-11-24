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

n = 10

edge_diff = []
jacc_sim = []

for i in range(0, n):
    total_sim = 0
    for k in range(10):
        g = nx.gnm_random_graph(10,15)
        shingles = shingle(g)
        signature = HashUtils.minhash(set(shingles), num_hashes=10000)

        h = g.copy()
        GraphUtils.randomise_labels(h)

        edges = list(nx.edges(h))
        nonedges = list(nx.non_edges(h))

        for j in range(i):
            if random() < 0.5:
                edge = choice(edges)
                h.remove_edge(edge[0], edge[1])
                edges.remove(edge)
            else:
                edge = choice(nonedges)
                h.add_edge(edge[0], edge[1])
                nonedges.remove(edge)
                

        shingles2 = shingle(h)
        signature2 = HashUtils.minhash(set(shingles2), num_hashes=10000)   

        minhash_sim = HashUtils.minhash_jaccard_similarity(signature, signature2, num_hashes=10000)
        edit_dist = nx.graph_edit_distance(g, h, 
            node_subst_cost=lambda u, v: 0,
            node_del_cost=lambda u: float('inf'),
            node_ins_cost=lambda v: float('inf'),
            edge_subst_cost=lambda e1, e2: 0,
            edge_del_cost=lambda e: 1,
            edge_ins_cost=lambda e: 1
        )
        print(f"{i} edge diff edit Distance: {edit_dist}, MinHash Jaccard Similarity: {minhash_sim}")

        # total_sim += minhash_sim
        edge_diff.append(edit_dist)
        jacc_sim.append(minhash_sim)

plt.scatter(edge_diff, jacc_sim, label="LSH Hashing",  marker='x')
plt.xlabel('Restricted GED', fontsize=14)
plt.ylabel('Jaccard Similarity', fontsize=14)   
plt.title('Restricted GED vs Jaccard Similarity predicted', fontsize=14)
plt.grid(True)
plt.legend()
plt.savefig("sim-mix.png", dpi=300)

# Graph base size of 100 nodes, 50 edges