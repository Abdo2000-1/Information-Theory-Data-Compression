def lz77_compress(text, window=10, lookahead=10) -> list:
    res = []
    i = 0

    while i < len(text):
        length, position = 0, 0

        for j in range(max(0, i - window), i):
            left = 0
            while (left < lookahead and i + left < len(text) - 1
                   and text[j + left] == text[i + left]):
                left += 1

            if left > length:          
                length = left
                position = i - j     
       
        res.append((position, length, text[i + length]))
        i += length + 1

    return res