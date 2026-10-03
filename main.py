from compressor import lz77_compress

def sizes(text) -> None :
    res = lz77_compress(text, window=10, lookahead=10) 
    
    if not res :
        print("Before: 0 bits")
        print("After:  0 bits")
        return 
    
    size_before = len(text) * 8
    print(f"Size before compression : {size_before}")
    
    max_offset = max(t[0] for t in res)
    max_length = max(t[1] for t in res)
    offset_bits = max(1, max_offset.bit_length())
    length_bits = max(1, max_length.bit_length())
    size_after = len(res) * (offset_bits + length_bits + 8)
    print('#' * 20)
    print(f"Size after compression : {size_after}")

if __name__ == "__main__":
    text = "ABAABABAABBBBBBBBBBBBA"
    res = lz77_compress(text, window=10, lookahead=10)
    print("Tokens:", res)
    
    print('#' * 20)
    
    sizes(text)