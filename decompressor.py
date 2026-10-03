
tages = []
n = int(input('Enter number of tuples: '))
for i in range (n):
    offset, length, char = input("Enter offset, length, char: ").split(',')
    offset = int(offset)
    length = int(length)
    tages.append((offset, length, char))
result = ''
for offset, length, char in tages:
    for l in range(length):
        result += result[len(result) - offset]
    result += char
print(result)