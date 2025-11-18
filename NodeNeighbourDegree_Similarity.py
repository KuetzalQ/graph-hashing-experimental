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

n = 5

for i in range(n):
    g = nx.gnm_random_graph(10,20)
    shingles = shingle(g)
    signature = HashUtils.minhash(set(shingles), num_hashes=64)

    h = g.copy()
    GraphUtils.randomise_labels(h)
    GraphUtils.remove_random_edge(h)
    # GraphUtils.add_random_edge(h)

    shingles2 = shingle(h)
    signature2 = HashUtils.minhash(set(shingles2), num_hashes=64)   

    minhash_sim = HashUtils.minhash_jaccard_similarity(signature, signature2, num_hashes=64)
    edit_dist = nx.graph_edit_distance(g, h)
    print(f"One edge diff edit Distance: {edit_dist}, MinHash Jaccard Similarity: {minhash_sim}")

    h = nx.gnm_random_graph(10,20)
    shingles2 = shingle(h)
    signature2 = HashUtils.minhash(set(shingles2), num_hashes=64)
    minhash_sim = HashUtils.minhash_jaccard_similarity(signature, signature2, num_hashes=64)
    edit_dist = nx.graph_edit_distance(g, h)
    print(f"Random graph edit Distance: {edit_dist}, MinHash Jaccard Similarity: {minhash_sim}")