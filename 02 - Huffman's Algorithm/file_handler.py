import pickle

class FileHandler:
    @staticmethod
    def read_text_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_text_file(filepath, text):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

    @staticmethod
    def save_compressed_file(filepath, bit_string, codes, original_codes, others_symbols):
        # حساب الـ Padding لضمان أن طول الـ Bit string يقبل القسمة على 8
        padding = (8 - len(bit_string) % 8) % 8
        bit_string_padded = bit_string + ("0" * padding)

        # تحويل سلسلة 0 و 1 إلى Bytes حقيقية
        byte_arr = bytearray()
        for i in range(0, len(bit_string_padded), 8):
            byte = bit_string_padded[i:i+8]
            byte_arr.append(int(byte, 2))

        # الـ Overhead / Metadata المسموح بحفظها بأي شكل
        header = {
            'codes': codes,
            'original_codes': original_codes,
            'others_symbols': others_symbols,
            'padding': padding
        }

        with open(filepath, 'wb') as f:
            pickle.dump(header, f)
            f.write(bytes(byte_arr))

    @staticmethod
    def load_compressed_file(filepath):
        with open(filepath, 'rb') as f:
            header = pickle.load(f)
            compressed_bytes = f.read()

        # إعادة تحويل الـ Bytes إلى سلسلة Bits
        bit_string = "".join(f"{b:08b}" for b in compressed_bytes)

        return bit_string, header['codes'], header['original_codes'], header['padding']