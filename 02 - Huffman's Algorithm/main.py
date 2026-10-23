from huffman import Huffman
from compressor import Compressor
from decompressor import Decompressor
from file_handler import FileHandler


if __name__ == "__main__":
    limit_val = float(input("Enter Minimum Limit of Symbol Probabilities (e.g. 0.05): "))

    input_file = "input.txt"
    compressed_file = "compressed.bin"
    output_file = "decompressed.txt"

    raw_text = FileHandler.read_text_file(input_file)

    huffman = Huffman(raw_text, limit=limit_val)
    huffman.calculate_frequencies()
    huffman.calculate_probabilities()
    huffman.prepare_huffman_symbols()
    huffman.build_huffman_tree()
    huffman.generate_codes()
    huffman.generate_original_codes()

    compressor = Compressor(huffman)
    compressed_bit_string = compressor.compress()

    FileHandler.save_compressed_file(compressed_file, compressed_bit_string, huffman.codes, huffman.original_codes, huffman.others_symbols)

    bit_string, codes, original_codes, padding = FileHandler.load_compressed_file(compressed_file)
    decompressor = Decompressor(bit_string, codes, original_codes, padding)
    decompressed_text = decompressor.decompress()

    FileHandler.write_text_file(output_file, decompressed_text)

    print("Compression and Decompression completed successfully.")