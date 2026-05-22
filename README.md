## Arithmetic coding project

# Arithmetic Coding vs Huffman Coding

This project implements:

- Arithmetic Encoding
- Arithmetic Decoding
- Huffman Coding

for a source with the following symbol probabilities:

| Symbol | Probability |
| ------ | ----------- |
| a      | 0.4         |
| b      | 0.3         |
| c      | 0.2         |
| d      | 0.1         |

The program generates a random sequence of 100 symbols from the alphabet:

```text
{a, b, c, d}
```

and compares:

- Arithmetic coding compressed size
- Huffman coding compressed size

---

# Theory

The symbols are assumed to be independent:

```math
P(a_1, a_2) = P(a_1)P(a_2)
```

Arithmetic coding compresses the entire message into a single interval between 0 and 1.

Huffman coding assigns shorter binary codes to more probable symbols.

Arithmetic coding usually achieves compression closer to the entropy limit.

---

# Implementation

Arithmetic coding is implemented manually without external libraries.

# How To Run

Open a terminal inside the project folder and run:

```bash
py index.py
```

or:

```bash
python index.py
```

---

# Program Output

The program outputs:

- Generated random sequence
- Arithmetic encoded value
- Verification of decoded sequence
- Huffman codes
- Number of bits used by arithmetic coding
- Number of bits used by Huffman coding
- Final comparison

Example:

```text
Decoded correctly:
True
```

This confirms that arithmetic decoding reconstructed the original sequence successfully.

---

## Correctness

The implementation is correct if:

```text
Decoded correctly: True
```

appears in the output.

This means:

```text
decoded_sequence == original_sequence
```

---

## Compression Comparison

Compare:

```text
Arithmetic coding bits
```

and

```text
Huffman coding bits
```
