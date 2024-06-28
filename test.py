# linkedin question
# given an urn (2 red 1 blue balls)
# draw balls, if red, put back a blue, if blue put back a blue
# how many draws until they are all blue?

from random import randint

SIMULATIONS = 1000000


def main():
    draws = 0
    for _ in range(SIMULATIONS):
        # True is blue, red is False
        bag = [False, False, True]
        while False in bag:
            draws += 1
            bag.pop(randint(0, 2))
            bag.append(True)
    print(f"Average draws: {draws / SIMULATIONS}")


if __name__ == "__main__":
    main()
