N = 10000000
# 1 is not considered, [2, 100]
primes = [True] * (N - 1)

for idx, prime in enumerate(primes):
    if not prime:
        continue
    print(idx + 2)

    # + 2 since we start at 2
    mod = idx + 2
    composite = 2 * (mod)
    while composite <= N:
        primes[composite - 2] = False
        composite += mod
