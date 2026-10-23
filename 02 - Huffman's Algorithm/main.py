from huffman import Huffman

text = "a b c a z d a f c q d a d c u a b a p d"

huffman = Huffman(text, limit=0.05)

huffman.calculate_frequencies()
huffman.calculate_probabilities()
huffman.prepare_huffman_symbols()

print("Frequencies:", dict(huffman.frequencies))
print("Common symbols:", huffman.common_symbols)
print("Rare symbols:", huffman.others_symbols)
print("Others probability:", huffman.others_probability)
print("Huffman symbols:", huffman.huffman_symbols)

huffman.build_huffman_tree()
huffman.generate_codes()

print("Huffman codes:", huffman.codes)
print("Root probability:", huffman.root.probability)
