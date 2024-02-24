# n between 0 and 100
# cannon 50 in 2 secs
# people 5 m/s

# 25.0 100.0
# 190.0 57.5
# 4
# 125.0 67.5
# 75.0 125.0
# 45.0 72.5
# 185.0 102.5

# plan

# collect all coords
# label them A-Z

# simulate all orders
# i.e. straight to Z or not

# calculate time to do the order
# (distance between points) - travel time

# return best time


def main():
    player, finish, cannons = read_coords()


def read_coords():
    player = read_coord(input(""))
    finish = read_coord(input(""))

    cannon_count = int(input(""))
    cannons = []

    for _ in range(cannon_count):
        cannons.append(read_coord(input("")))

    return player, finish, cannons


def read_coord(coordinate_string):
    """
    returns tuple version of coord string
    """
    x, y = coordinate_string.split(" ")
    return (float(x), float(y))


if __name__ == "__main__":
    main()
