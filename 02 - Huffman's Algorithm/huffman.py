from collections import defaultdict
from itertools import count
import heapq
from node import Node


class Huffman:
    def __init__(self, text, limit=0.05):
        self.text = text.split()
        self.limit = limit
        self.len_text = len(self.text)

        self.frequencies = defaultdict(int)
        self.probabilities = {}
        self.common_symbols = {}
        self.others_symbols = {}
        self.others_probability = 0

        self.huffman_symbols = {}
        self.heap = []
        self.root = None

    def calculate_frequencies(self):
        for char in self.text:
            self.frequencies[char] += 1

    def calculate_probabilities(self):
        for char, frequency in self.frequencies.items():
            probability = frequency / self.len_text

            if probability <= self.limit:
                self.others_symbols[char] = probability
                self.others_probability += probability
            else:
                self.probabilities[char] = probability
                self.common_symbols[char] = probability

    def prepare_huffman_symbols(self):
        for char, probability in self.common_symbols.items():
            self.huffman_symbols[char] = probability

        if self.others_symbols:
            self.huffman_symbols["Others"] = self.others_probability

    def build_huffman_tree(self):
        self.heap = []
        unique_id = count()

        for symbol, probability in self.huffman_symbols.items():
            node = Node(probability, symbol)
            heapq.heappush(
                self.heap,
                (probability, next(unique_id), node)
            )

        if not self.heap:
            raise ValueError("Cannot build a Huffman tree without symbols.")

        while len(self.heap) > 1:
            p1, id1 , node1 = heapq.heappop(self.heap)
            p2, id2 , node2 = heapq.heappop(self.heap)

            parent = Node(
                p1 + p2,
                left=node1,
                right=node2
            )

            heapq.heappush(
                self.heap,
                (parent.probability, next(unique_id), parent)
            )

        self.root = self.heap[0][2]
        return self.root

