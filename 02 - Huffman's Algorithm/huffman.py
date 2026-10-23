import math
from node import Node


class Huffman:
    def __init__(self, text, limit=0.05):
        self.text = text.split()
        self.limit = limit
        self.len_text = len(self.text)

        self.frequencies = {}
        self.probabilities = {}
        self.common_symbols = {}
        self.others_symbols = {}
        self.others_probability = 0

        self.huffman_symbols = {}
        self.nodes = []
        self.root = None

        self.codes = {}
        self.original_codes = {}

    def calculate_frequencies(self):
        for char in self.text:
            if char in self.frequencies:
                self.frequencies[char] += 1
            else:
                self.frequencies[char] = 1

    def calculate_probabilities(self):
        for char in self.frequencies:
            frequency = self.frequencies[char]
            probability = frequency / self.len_text

            if probability <= self.limit:
                self.others_symbols[char] = probability
                self.others_probability += probability
            else:
                self.probabilities[char] = probability
                self.common_symbols[char] = probability

    def prepare_huffman_symbols(self):
        for char in self.common_symbols:
            self.huffman_symbols[char] = self.common_symbols[char]

        if len(self.others_symbols) > 0:
            self.huffman_symbols["Others"] = self.others_probability

    def build_huffman_tree(self):
        self.nodes = []

        for symbol in self.huffman_symbols:
            probability = self.huffman_symbols[symbol]
            node = Node(probability, symbol)
            self.nodes.append(node)

        if len(self.nodes) == 0:
            raise ValueError("Cannot build a Huffman tree without symbols.")

        while len(self.nodes) > 1:

            self.nodes.sort(key=lambda x: x.probability)


            node1 = self.nodes.pop(0)
            node2 = self.nodes.pop(0)

     
            parent = Node(
                node1.probability + node2.probability,
                left=node1,
                right=node2
            )
            self.nodes.append(parent)

        self.root = self.nodes[0]
        return self.root

    def _generate_codes_recursive(self, node, code):
        if node.left is None and node.right is None:
            self.codes[node.symbol] = code

        if node.left is not None:
            self._generate_codes_recursive(node.left, code + "0")

        if node.right is not None:
            self._generate_codes_recursive(node.right, code + "1")

    def generate_codes(self):
        self.codes = {}
        self._generate_codes_recursive(self.root, "")

    def generate_original_codes(self):
        symbols = sorted(self.frequencies.keys())

        bits = math.ceil(math.log2(len(symbols)))
        if bits < 1:
            bits = 1

        self.original_codes = {}
        for i in range(len(symbols)):
            symbol = symbols[i]

            self.original_codes[symbol] = bin(i)[2:].zfill(bits)