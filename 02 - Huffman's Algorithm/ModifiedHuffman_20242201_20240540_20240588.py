import math
import pickle


class Node:
    def __init__(self, probability, symbol='', left=None, right=None):
        self.left = left
        self.right = right
        self.probability = probability
        self.symbol = symbol


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


class Compressor:
    def __init__(self, huffman):
        self.huffman = huffman

    def compress(self):
        text_binary_code = []

        for char in self.huffman.text:
            if char in self.huffman.others_symbols:
                text_binary_code.append(
                    self.huffman.codes["Others"]
                    + self.huffman.original_codes[char]
                )
            else:
                text_binary_code.append(
                    self.huffman.codes[char]
                )

        return "".join(text_binary_code)


class Decompressor:
    def __init__(self, bit_string, codes, original_codes, padding):
        self.bit_string = bit_string
        self.codes = codes
        self.original_codes = original_codes
        self.padding = padding

    def decompress(self):
        if self.padding > 0:
            bit_string = self.bit_string[:-self.padding]
        else:
            bit_string = self.bit_string

   
        rev_codes = {}
        for k in self.codes:
            rev_codes[self.codes[k]] = k

        rev_original = {}
        fixed_bits = 0
        for k in self.original_codes:
            code_val = self.original_codes[k]
            rev_original[code_val] = k
            fixed_bits = len(code_val)

        decompressed_text = []
        current_code = ""
        idx = 0
        n = len(bit_string)

        while idx < n:
            current_code += bit_string[idx]
            idx += 1

            if current_code in rev_codes:
                symbol = rev_codes[current_code]
                if symbol == "Others":
                    other_code = bit_string[idx : idx + fixed_bits]
                    idx += fixed_bits
                    decompressed_text.append(rev_original[other_code])
                else:
                    decompressed_text.append(symbol)
                current_code = ""

        return " ".join(decompressed_text)


def save_compressed_file(filepath, bit_string, codes, original_codes, others_symbols):
    padding = (8 - len(bit_string) % 8) % 8
    bit_string_padded = bit_string + ("0" * padding)

    byte_list = []
    for i in range(0, len(bit_string_padded), 8):
        byte = bit_string_padded[i : i + 8]
        byte_list.append(int(byte, 2))

    header = {
        'codes': codes,
        'original_codes': original_codes,
        'others_symbols': others_symbols,
        'padding': padding
    }

    with open(filepath, 'wb') as f:
        pickle.dump(header, f)
        f.write(bytes(byte_list))


def load_compressed_file(filepath):
    with open(filepath, 'rb') as f:
        header = pickle.load(f)
        compressed_bytes = f.read()

    bit_parts = []
    for b in compressed_bytes:
        bit_parts.append(bin(b)[2:].zfill(8))

    bit_string = "".join(bit_parts)

    return bit_string, header['codes'], header['original_codes'], header['padding']


if __name__ == "__main__":

    limit_val = float(input("Enter Minimum Limit of Symbol Probabilities (e.g. 0.05): "))

    input_file = "input.txt"
    compressed_file = "compressed.bin"
    output_file = "decompressed.txt"

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    huffman = Huffman(raw_text, limit=limit_val)
    huffman.calculate_frequencies()
    huffman.calculate_probabilities()
    huffman.prepare_huffman_symbols()
    huffman.build_huffman_tree()
    huffman.generate_codes()
    huffman.generate_original_codes()

    compressor = Compressor(huffman)
    compressed_bit_string = compressor.compress()

    save_compressed_file(compressed_file, compressed_bit_string, huffman.codes, huffman.original_codes, huffman.others_symbols)

    bit_string, codes, original_codes, padding = load_compressed_file(compressed_file)
    decompressor = Decompressor(bit_string, codes, original_codes, padding)
    decompressed_text = decompressor.decompress()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decompressed_text)

    print("Compression and Decompression completed successfully.")