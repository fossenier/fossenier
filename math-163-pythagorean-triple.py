import math as m


def pythagorean_triple(n):
    """
    This will take a number n and return all pairs of integers (p,q) such that,
    p^2 - q^2 = n or p^2 + q^2 = n. This is a brute force method.

    Args:
        n (`int`): Any whole positive number.

    Returns:
        `List(List(int)), List(List(int))`: Value pairs satisfying the criteria.
    """
    a = []
    b = []
    for p in range(1, n):
        for q in range(1, n):
            # save valid pairs of p and q
            if p**2 - q**2 == n:
                a.append([p, q])
            if p**2 + q**2 == n:
                entry = sorted([p, q])
                if entry not in b:
                    b.append(entry)

    return a, b


print(pythagorean_triple(2023))
