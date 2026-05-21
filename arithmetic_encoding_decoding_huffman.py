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