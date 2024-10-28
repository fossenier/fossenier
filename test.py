import math
import random


def map_poly(storage: dict[str, float], x: float) -> float:
    """
    Computes the polynomial based on the given storage dictionary and base.

    Parameters:
    storage (dict): A dictionary where keys are letters ('a' to 'z') and values are numerical coefficients.
    x (float): The base to raise to the power based on the letter positions.

    Returns:
    float: The result of the polynomial sum.
    """
    polynomial = 0.0

    # Iterate over the first 26 lowercase letters, if present in storage
    for i in range(26):
        letter = chr(ord("a") + i)  # Convert index to corresponding letter
        if letter in storage:
            # Add the current letter's value * (x ^ i)
            polynomial += storage[letter] * math.pow(x, i)

    return polynomial


# Example usage
alphabet = "abcdefghijklmnopqrstuvwxyz"
storage = {c: i for i, c in enumerate(alphabet)}  # Create example dictionary
x = random.uniform(1.0, 5.0)  # Random base value between 1.0 and 5.0
x = 3.25

result = map_poly(storage, x)
print(f"The polynomial result for base {x} is: {result}")

222297527137285
222297527137285.250000
