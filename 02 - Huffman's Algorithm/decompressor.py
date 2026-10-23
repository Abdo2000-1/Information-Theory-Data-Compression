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