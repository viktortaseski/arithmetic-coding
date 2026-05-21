import random
import math
import heapq
from collections import Counter

# =========================================================
# PROBABILITIES
# =========================================================

probabilities = {
    'a': 0.4,
    'b': 0.3,
    'c': 0.2,
    'd': 0.1
}

symbols = list(probabilities.keys())
weights = list(probabilities.values())

# =========================================================
# GENERATE RANDOM SEQUENCE
# =========================================================

sequence = random.choices(symbols, weights=weights, k=100)
sequence = ''.join(sequence)

print("Generated sequence:")
print(sequence)
print()