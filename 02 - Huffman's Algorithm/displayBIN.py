import pickle

with open("compressed.bin", "rb") as f:

    header = pickle.load(f)

    compressed_bytes = f.read()

print("--- 1. Header Content (Overhead) ---")
print("Huffman Codes:", header['codes'])
print("Original Fixed Codes:", header['original_codes'])
print("Others Symbols:", header['others_symbols'])
print("Padding Bits:", header['padding'])

print("\n--- 2. Raw Compressed Bytes ---")
print("Bytes Object:", compressed_bytes)
print("Number of Bytes:", len(compressed_bytes))


bits_with_padding = "".join(bin(b)[2:].zfill(8) for b in compressed_bytes)
actual_bits = bits_with_padding[:-header['padding']] if header['padding'] > 0 else bits_with_padding

print("\n--- 3. Binary Stream (0s and 1s) ---")
print("Bits in file (with padding):", bits_with_padding)
print("Actual Compressed Bits:     ", actual_bits)