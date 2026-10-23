from huffman import Huffman 

class Compressor :
    def __init__(self , huffman):
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