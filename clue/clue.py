"""
This is a second slice of Clue that is focused on simply giving instructions.
"""


class Clue:
    def __init__(self, game_path):
        self.rooms = []
        self.suspects = []
        self.weapons = []
        self.suspect_order = []
        self.cpu_suspect = None

        self.__read_board(game_path)

    def __read_board(self, game_path):
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
                            self.suspects.append(tile)
                        # otherwise it's a room
                        else:
                            if tile not in self.rooms:
                                self.rooms.append(tile)

    def __get_game_order(self):
        valid_order = False
        # get the order of the players
        while not valid_order:
            print("Enter the order of the players, separated by commas.")
            order = [suspect.strip() for suspect in input().split(",")]
            valid_suspects = []

            checklist = self.suspects.copy()
            for suspect in order:
                # check if the suspect is valid
                for check in checklist:
                    # it is valid
                    if suspect.lower() in check.lower():
                        valid_suspects.append(check)
                        checklist.remove(check)
                        break

            # make sure 2 or more players are in the game
            if len(self.suspects) - len(checklist) < 2:
                print(f"Error: you must have at least 2 players.")
                continue

            # the suspects left in the checklist are unused
            self.suspect_order = valid_suspects
            valid_order = True

    def __get_cpu_suspect(self):
        cpu_suspect = None
        while cpu_suspect not in self.suspect_order:
            cpu_suspect = input(f"Enter the CPU suspect({self.suspect_order}): ")

        self.cpu_suspect = cpu_suspect

    def initialize_game(self):
        print("Welcome to Clue!")
        self.__get_game_order()
        self.__get_cpu_suspect()


def main():
    game = Clue("board.csv")
    game.initialize_game()


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
