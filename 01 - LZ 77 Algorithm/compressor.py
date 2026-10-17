def lz77_compress(text, window=10, lookahead=10):
    res = []
    i = 0

    while i < len(text):

        length = 0
        position = 0
        start = max(0, i - window)
        max_length = min(lookahead, len(text) - i - 1) # handling the Reapetative Seq.

        for j in range(start, i):
            left = 0

            while (
                left < max_length
                and text[j + left] == text[i + left]
            ):
                left += 1

            if left > length:
                length = left
                position = i - j

         
        next_char = text[i + length]

        res.append((position, length, next_char))

        
        i += length + 1

    return res

def tag_to_binary(tag):
    position, length, next_char = tag

    position_bits = format(position, "04b")
    length_bits = format(length, "04b")
    symbol_bits = format(ord(next_char), "08b")

    return position_bits + length_bits + symbol_bits



with open("file1.txt", "r", encoding="ascii") as file:
    text = file.read()

res = lz77_compress(text)

with open("file2.txt", "w", encoding="ascii") as file:
    for tag in res:
        position, length, next_char = tag
        binary = tag_to_binary(tag)

        file.write(
            f"({position}, {length}, {next_char!r}) | {binary}\n"
        )

print("Compression completed!")
print("Compressed tags saved in file2.txt")