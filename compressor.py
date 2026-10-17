def lz77_compress(text, window=10, lookahead=10):
    res = []
    i = 0

    while i < len(text):

        length = 0
        position = 0
        start = max(0, i - window)

        for j in range(start, i):
            left = 0

            while (
                left < lookahead
                and i + left < len(text)
                and j + left < i
                and text[j + left] == text[i + left]
            ):
                left += 1
            if left > length:
                length = left
                position = i - j

         
        if i + length < len(text):
            next_char = text[i + length]
        else:
            next_char = ""

        res.append((position, length, next_char))

        
        i += length + 1

    return res