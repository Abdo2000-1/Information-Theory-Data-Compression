from huffman import Huffman 
from node import Node
import heapq
text = "a b c a z d a f c q d a d c u a b a p d"


a = Node(0.30, 'a')
b = Node(0.10, 'b')
c = Node(0.15, 'c')
d = Node(0.20, 'd')

heap = [
    (a.probability, a),
    (b.probability, b),
    (c.probability, c),
    (d.probability, d)
]

heapq.heapify(heap)

probability, node = heapq.heappop(heap)
print(node.symbol) # min p in heap = 0.10

probability, node = heapq.heappop(heap)
print(node.symbol) 


huffman = Huffman(text)

huffman.calculate_frequencies()
huffman.calculate_probabilities()
huffman.prepare_huffman_symbols()

print("Frequencies:", dict(huffman.frequencies))
print("Common symbols:", huffman.common_symbols)
print("Others symbols:", huffman.others_symbols)
print("Others probability:", huffman.others_probability)

print(huffman.huffman_symbols)