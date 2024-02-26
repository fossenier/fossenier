expected_locations = {
    "A": (0, 0),
    "B": (1, 0),
    "C": (2, 0),
    "D": (3, 0),
    "E": (0, 1),
    "F": (1, 1),
    "G": (2, 1),
    "H": (3, 1),
    "I": (0, 2),
    "J": (1, 2),
    "K": (2, 2),
    "L": (3, 2),
    "M": (0, 3),
    "N": (1, 3),
    "O": (2, 3),
}

# collect grid from user
grid = []
for _ in range(4):
    # save row, ignore the empty square
    grid.append(input(""))

# assess each character for its scatter
scatter = 0
for y_coord, letter_row in enumerate(grid):
    for x_coord, letter in enumerate(letter_row):
        # determine expected locations
        if letter == ".":
            continue
        x_expected, y_expected = expected_locations[letter]
        # calculate discrepancy
        y_scatter = abs(y_coord - y_expected)
        x_scatter = abs(x_coord - x_expected)
        # tally it
        scatter += y_scatter + x_scatter

print(scatter)
