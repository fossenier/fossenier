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
    last_replaced = "x"
    last_coords = (0, 0)
    while True:
        new_coords = [int(num) for num in input("Enter x, y: ").split(",")]
        board[last_coords[1]][last_coords[0]] = last_replaced
        last_replaced = board[new_coords[1]][new_coords[0]]
        last_coords = new_coords
        board[new_coords[1]][new_coords[0]] = "X"
        draw_board("clue_board_1.png", board)


def proto_print_board():
    with open("clue_board_1.csv", "r") as f:
        for line in f:
            print(line)


def read_board(filename):
    with open(filename, "r") as f:
        board = []
        for line in f:
            row = line.rstrip("\n").split(",")
            board.append(row)
    return board


def draw_board(filename, board):
    """
    Creates an image of the board and saves it to a file with coloured tiles and
    text annotations.
    """
    from PIL import Image, ImageDraw, ImageFont

    def get_tile_color(tile):
        """Returns the color corresponding to the tile type."""
        tile_colors = {
            "x": (40, 39, 41),  # walls are dark gray
            " ": (226, 200, 60),  # floors are classic yellow
        }
        return tile_colors.get(tile, (255, 0, 0))  # use red for all other tiles

    cell_size = 50
    cell_border = 2
    font_size = 12

    width, height = len(board[0]) * cell_size, len(board) * cell_size

    img = Image.new("RGBA", (width, height), "black")
    draw = ImageDraw.Draw(img)
    try:
        # attempt to load a truetype or opentype font file
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # fall back to a default font if unable to load
        font = ImageFont.load_default()

    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            fill = get_tile_color(tile)
            top_left = (j * cell_size + cell_border, i * cell_size + cell_border)
            bottom_right = (
                (j + 1) * cell_size - cell_border,
                (i + 1) * cell_size - cell_border,
            )
            draw.rectangle([top_left, bottom_right], fill=fill)

            # check if tile needs text
            if tile not in ["x", " "]:  # floors and walls don't need text
                text_position = (
                    j * cell_size + cell_size // 2,
                    i * cell_size + cell_size // 2,
                )
                draw.text(text_position, tile, font=font, anchor="mm", fill="black")

    img.save(filename)
    print(f"Board drawn and saved as {filename}")


if __name__ == "__main__":
    main()
