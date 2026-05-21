import random
import math
import heapq
from decimal import Decimal, getcontext

# =========================================================
# HIGH PRECISION FOR ARITHMETIC CODING
# =========================================================

getcontext().prec = 300

# =========================================================
# PROBABILITIES
# =========================================================

probabilities = {
    'a': Decimal('0.4'),
    'b': Decimal('0.3'),
    'c': Decimal('0.2'),
    'd': Decimal('0.1')
}

symbols = list(probabilities.keys())
weights = [float(p) for p in probabilities.values()]

# =========================================================
# GENERATE RANDOM SEQUENCE
# =========================================================

sequence = random.choices(symbols, weights=weights, k=100)
sequence = ''.join(sequence)

print("Generated sequence:")
print(sequence)
print()

# =========================================================
# BUILD CUMULATIVE INTERVALS
# =========================================================

cumulative = {}

low = Decimal('0')

for symbol, prob in probabilities.items():
    cumulative[symbol] = (low, low + prob)
    low += prob

# =========================================================
# ARITHMETIC ENCODING
# =========================================================

def arithmetic_encode(message):

    low = Decimal('0')
    high = Decimal('1')

    for symbol in message:

        range_width = high - low

        sym_low, sym_high = cumulative[symbol]

        old_low = low

        high = old_low + range_width * sym_high
        low = old_low + range_width * sym_low

    code = (low + high) / Decimal('2')

    return code, low, high

# =========================================================
# ARITHMETIC DECODING
# =========================================================

def arithmetic_decode(code, length):

    decoded = ""

    low = Decimal('0')
    high = Decimal('1')

    for _ in range(length):

        range_width = high - low

        value = (code - low) / range_width

        for symbol, (sym_low, sym_high) in cumulative.items():

            if sym_low <= value < sym_high:

                decoded += symbol

                old_low = low

                high = old_low + range_width * sym_high
                low = old_low + range_width * sym_low

                break

    return decoded

# =========================================================
# RUN ARITHMETIC CODING
# =========================================================

code, low_interval, high_interval = arithmetic_encode(sequence)

decoded_sequence = arithmetic_decode(code, len(sequence))

print("Arithmetic Coding")
print("------------------")
print("Encoded value:")
print(code)
print()

print("Decoded correctly:")
print(decoded_sequence == sequence)
print()

# estimate bits needed
interval_size = high_interval - low_interval
arith_bits = math.ceil(-math.log2(float(interval_size)))

print("Estimated arithmetic coding bits:")
print(arith_bits)
print()

# =========================================================
# HUFFMAN CODING
# =========================================================

class Node:

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freqs):

    heap = [Node(char, float(freq)) for char, freq in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:

        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)

        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, current="", codes=None):

    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current

    generate_codes(node.left, current + "0", codes)
    generate_codes(node.right, current + "1", codes)

    return codes

tree = build_huffman_tree(probabilities)

codes = generate_codes(tree)

print("Huffman Codes")
print("--------------")

for symbol, codeword in codes.items():
    print(symbol, ":", codeword)

encoded_huffman = ''.join(codes[ch] for ch in sequence)

print()
print("Huffman encoded length:")
print(len(encoded_huffman), "bits")

# =========================================================
# COMPARISON
# =========================================================

print()
print("Comparison")
print("----------")

print("Arithmetic coding bits :", arith_bits)
print("Huffman coding bits    :", len(encoded_huffman))

if arith_bits < len(encoded_huffman):
    print("Arithmetic coding is better.")

elif arith_bits > len(encoded_huffman):
    print("Huffman coding is better.")

else:
    print("Both methods are equal.")