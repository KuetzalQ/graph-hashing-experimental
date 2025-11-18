def minhash(input_set, num_hashes=10):
    min_hashes = [float('inf')] * num_hashes

    for i in range(num_hashes):
        for item in input_set:
            # Create hash using item and hash function index
            hash_value = hash((item, i)) % (2**32)
            min_hashes[i] = min(min_hashes[i], hash_value)

    signature = 0
    for i, min_hash in enumerate(min_hashes):
        if min_hash != float('inf'):
            signature ^= (int(min_hash) << (i % 32))
    
    return signature & ((1 << 64) - 1)

def minhash_jaccard_similarity(hash1, hash2, num_hashes=10):
    mismatches = bin(hash1 ^ hash2).count('1')  
    return (num_hashes-mismatches) / num_hashes