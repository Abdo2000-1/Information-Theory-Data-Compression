from huffman import Huffman
from compressor import Compressor

text = "a b c a z d a f c q d a d c u a b a p d"

huffman = Huffman(text)

huffman.calculate_frequencies()
huffman.calculate_probabilities()
huffman.prepare_huffman_symbols()
huffman.build_huffman_tree()
huffman.generate_codes()
huffman.generate_original_codes()

compressor = Compressor(huffman)

compressed_text = compressor.compress()

print("Huffman codes:", huffman.codes)
print("#"*50)
print("Original codes:", huffman.original_codes)
print("#"*50)
print("Rare symbols:", huffman.others_symbols)
print("#"*50)
print("Compressed text:", compressed_text)