"""
This is a second slice of Clue that is focused on simply giving instructions.
"""


class Clue:
    def __init__(self, game_path):
        self.board = []  # the game board
        self.cpu_location = (None, None)  # the CPU location
        self.cpu_suspect = None  # the CPU suspect
        self.rooms = []  # list of room names
        self.suspects = {}  # key: suspect name, value: (x, y) starting position
        self.suspect_order = []  # the order of the players
        self.weapons = []  # list of weapon names

        self.__read_board_data(game_path)

    def __get_tile_position(self, tile):
        """
        Purpose:
            Get the position of a tile on the board.
        Pre-conditions:
            str tile: the tile to find.
        Post-conditions:
            tuple: the position of the tile.
        Returns:
            tuple: the position of the tile.
        """
        for y, row in enumerate(self.board):
            for x, board_tile in enumerate(row):
                if board_tile == tile:
                    return (x, y)

    def __prompt_cpu_suspect(self):
        """
        Purpose:
            Prompts the user to select the CPU suspect.
        Pre-conditions:
            self.suspect_order must have been populated.
        Post-conditions:
            self.cpu_suspect: the CPU suspect.
        Returns:
            None.
        """
        # get the CPU suspect from the user
        cpu_suspect = None
        while cpu_suspect not in self.suspect_order:
            cpu_suspect = input(f"Enter the CPU suspect({self.suspect_order}): ")

        # save to the object the suspect as named in self.suspect_order
        for suspect in self.suspect_order:
            if cpu_suspect.lower() in suspect.lower():
                self.cpu_suspect = suspect

    def __prompt_game_order(self):
        """
        Purpose:
            Prompts the user to enter the player order. The players entered must be
            contained as characters within the suspects list.
        Pre-conditions:
            self.suspects must have been populated.
        Post-conditions:
            self.suspect_order: a list of the suspects in the order they are playing.
        Returns:
            None.
        """
        is_valid_order = False
        # get the order of the players
        while not is_valid_order:
            print("Enter the order of the players, separated by commas.")
            user_order = [suspect.strip() for suspect in input().split(",")]
            validated_suspects = []

            actual_suspects = [key for key in self.suspects.keys()]
            for user_suspect in user_order:
                # check if the suspect is valid
                for actual_suspect in actual_suspects:
                    # accept the suspect if it is a substring of the actual suspect (Green -> Mr. Green)
                    if user_suspect.lower() in actual_suspect.lower():
                        validated_suspects.append(actual_suspect)
                        actual_suspects.remove(actual_suspect)
                        break

            # make sure 2 or more players are in the game
            if len(validated_suspects) < 2:
                print(
                    f"Error: you must have at least 2 valid players. You entered {validated_suspects}."
                )
                continue

            # use the validated order
            self.suspect_order = validated_suspects
            is_valid_order = True

    def __read_board_data(self, game_path):
        """
        Purpose:
            Read the clue game board from a specified path.
        Pre-conditions:
            str game_path: the path to the game board. MUST BE properly formatted.
        Post-conditions:
            self.board: a list of lists representing the game board (players are removed).
            self.rooms: all of the rooms in the game.
            self.suspects: all of the suspects in the game.
            self.weapons: all of the weapons in the game.
        Returns:
            None.
        """
        with open(game_path, "r") as f:
            # first line is weapons
            self.weapons = f.readline().rstrip().split(",")

            # the rest of the lines are the board
            tile_rows = f.readlines()
            for y_coord, tile_row in enumerate(tile_rows):
                tiles = tile_row.rstrip().split(",")
                for x_coord, tile in enumerate(tiles):

                    if tile not in [" ", "x", "Door"]:
                        # this is a suspect since it is on the edge
                        if (
                            y_coord == 0
                            or y_coord == len(tile_rows) - 1
                            or x_coord == 0
                            or x_coord == len(tiles) - 1
                        ):
                            self.suspects[tile] = (x_coord, y_coord)
                        # otherwise it's a room
                        else:
                            if tile not in self.rooms:
                                self.rooms.append(tile)

            # save the board to the object
            for line in f:
                # read row
                row = line.rstrip().split(",")
                # remove suspects from the board
                for i, tile in enumerate(row):
                    if tile in self.suspects.keys():
                        row[i] = " "
                self.board.append(row)

    def initialize_game(self):
        """
        Purpose:
            Initializes the game with the two required user inputs before the main loop.
        Pre-conditions:
            None.
        Post-conditions:
            self.suspect_order, self.cpu_suspect are populated.
        Returns:
            None.
        """
        print("Welcome to Clue!")
        self.__prompt_game_order()
        self.__prompt_cpu_suspect()

    def run_game(self):
        pass


def main():
    game = Clue("board.csv")
    game.initialize_game()
    game.run_game()


if __name__ == "__main__":
    main()


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
