# 17 13 9 12

import random

TOT = 100000


def simulate(req):
    return req <= sum([random.randint(1, 6) for _ in range(3)])


succeeded = 0
for _ in range(TOT):
    success = True
    for num in [17, 13, 9, 12]:
        success = simulate(num) and success

    if success:
        succeeded += 1

print(f"{1 / ((succeeded / TOT)):.9f}")
