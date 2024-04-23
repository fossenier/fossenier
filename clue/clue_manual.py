"""
This is a first slice of Clue that is hard-coded and manual.
"""

ROOMS = [
    "Ballroom",
    "Billiard Room",
    "Conservatory",
    "Dining Room",
    "Hall",
    "Kitchen",
    "Library",
    "Lounge",
    "Study",
]
SUSPECTS = [
    "Colonel Mustard",
    "Miss Scarlet",
    "Mr. Green",
    "Mrs. Peacock",
    "Mrs, White",
    "Professor Plum",
]
WEAPONS = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]

IMAGE = [
    [False, True, False, False, True, False],
    [False, False, True, False, False, True],
    [False, True, False, True, False, False],
    [False, False, True, False, True, False],
    [True, False, False, True, False, True],
    [False, True, False, False, True, False],
]


def main():
    board = read_board("clue_board_1.csv")
    draw_board("clue_board_1.png", board)
    # proto_print_board()


def proto_print_board():
    with open("clue_board_1.csv", "r") as f:
        for line in f:
            print(line)


def read_board(filename):
    with open(filename, "r") as f:
        board = []
        for line in f:
            row = line.strip().split(",")
            board.append(row)
    return board


def draw_board(filename, board):
    from PIL import Image, ImageDraw

    cell_size = 50
    cell_border = 2

    width, height = len(board[0]), len(board)

    # Create a blank canvas
    img = Image.new("RGBA", (width * cell_size, height * cell_size), "black")
    draw = ImageDraw.Draw(img)

    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == " ":
                fill = (226, 200, 60)
            elif tile == "x":
                fill = (40, 39, 41)

            draw.rectangle(
                (
                    [
                        (j * cell_size + cell_border, i * cell_size + cell_border),
                        (
                            (j + 1) * cell_size - cell_border,
                            (i + 1) * cell_size - cell_border,
                        ),
                    ]
                ),
                fill=fill,
            )

    img.save(filename)


if __name__ == "__main__":
    main()
