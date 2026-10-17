def binary_to_tag(binary):
    offset = int(binary[0:4], 2)
    length = int(binary[4:8], 2)
    next_char = chr(int(binary[8:16], 2))

    return offset, length, next_char


def lz77_decompress(input_file, output_file):

    result = ""

    with open(input_file, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            tag, binary = line.split("|", 1)

            binary = binary.strip()

            offset, length, next_char = binary_to_tag(binary)

            if length > 0:

                start = len(result) - offset

                for i in range(length):
                    result += result[start + i]

            if next_char != "":
                result += next_char

    with open(output_file, "w") as file:
        file.write(result)

    print("Decompression completed!")
    print("Original text:", result)


lz77_decompress("file2.txt", "decompressed.txt")