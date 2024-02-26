# get integer
number = int(input(""))

# convert to binary
binary_flipped = ""
while number > 0:
    # divide by 2, get remainder
    binary_flipped += str(number % 2)
    # take non remainder (13 / 2 = 6)
    number //= 2

# convert to int
base = 1
number = 0
for bit in reversed(binary_flipped):
    number += int(bit) * base
    base *= 2

# print number
print(number)
