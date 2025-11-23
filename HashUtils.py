import mmh3

def minhash(input_set, num_hashes=10):
    min_hashes = []

    for i in range(num_hashes):
        min_hash = float('inf')
        for item in input_set:
            # Create hash using item and hash function index
            hash_value = mmh3.hash(str(item), i, False)
            min_hash = min(min_hash, hash_value)
        min_hashes.append(min_hash)
    # signature = ""
    # for i, min_hash in enumerate(min_hashes):
    #     signature += str(min_hash)
    
    return tuple(min_hashes)

# def minhash(input_set, num_hashes=10):
#     min_hashes = [float('inf')] * num_hashes

#     for i in range(num_hashes):
#         for item in input_set:
#             # Create hash using item and hash function index
#             hash_value = hash((item, i)) % (2**32)
#             min_hashes[i] = min(min_hashes[i], hash_value)

#     signature = 0
#     for i, min_hash in enumerate(min_hashes):
#         if min_hash != float('inf'):
#             signature ^= (int(min_hash) << (i % 32))
    
#     return signature & ((1 << 64) - 1)

def minhash_jaccard_similarity(hash1, hash2, num_hashes=10):
    matches = 0

    for i in range(num_hashes):
        if (hash1[i] == hash2[i]):
            matches += 1

    return matches / num_hashes