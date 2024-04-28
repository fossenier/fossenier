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


def main():
    # read in the game board
    board = read_board("clue_board_1.csv")

    # display the board
    draw_board("clue_board_1.png", board)

    # take in all initial players
    player_positions = get_player_positions(board)
    (print(player_positions))
    input("Press enter to continue")
    draw_board("clue_board_1.png", board)

    # move a player
    while True:
        player = input("Enter player name: ")
        direction = input("Enter direction: ")
        player_positions[player] = move_player(
            board, player_positions[player], direction
        )
        print(player_positions)

    #
    # last_replaced = "x"
    # last_coords = (0, 0)
    # while True:
    #     new_coords = [int(num) for num in input("Enter x, y: ").split(",")]
    #     board[last_coords[1]][last_coords[0]] = last_replaced
    #     last_replaced = board[new_coords[1]][new_coords[0]]
    #     last_coords = new_coords
    #     board[new_coords[1]][new_coords[0]] = "X"
    #     draw_board("clue_board_1.png", board)


def move_player(board, player_position, direction):
    """
    Moves a player in a given direction on the board.
    """
    # get the player's current position
    x, y = player_position

    # determine the new position based on the direction
    if direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    elif direction == "left":
        x -= 1
    elif direction == "right":
        x += 1

    board_height = len(board)
    board_width = len(board[0])

    # check if the new position is within bounds and then check if it is valid
    if 0 <= x < board_width and 0 <= y < board_height:
        if board[y][x] == "x":
            print("You can't move there!")
        else:
            player_position = (x, y)
    else:
        print("That move is outside the board!")

    return player_position


def get_player_positions(board):
    """
    Returns a dictionary of player names and their positions on the board.
    """
    player_positions = {}
    for suspect in SUSPECTS:
        suspect = suspect.split(" ")[1]
        position = get_position(board, suspect)
        player_positions[suspect] = position
        print(suspect)
        print(position)
        set_position(board, " ", position)
    return player_positions


def set_position(board, tile, position):
    """
    Sets a given position to a new name.
    """
    board[position[1]][position[0]] = tile


def get_position(board, tile):
    """
    Finds in the board where a named tile is.
    """
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.startswith(tile):
                return (j, i)
    return None


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
