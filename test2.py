import math

nums = "23+17+34+26+18+33+46+42+13+37+44+16+22+19+28+32+18+39+40+48+25+36+23+39+42+46+29+17+24+31"

data = [int(x) for x in nums.split("+")]

mean = sum(data) / len(data)
sum = 0

for x in data:
    sum += (x - mean) ** 2

print(math.sqrt(sum / (len(data) - 1)))