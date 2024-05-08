"""
This is a module for the third slice of Clue.
It houses and manipulates all data regarding the board.
"""

from config import DOOR, HALL, WALL


class Board(object):
    def __init__(self, board_path):
        """
        Initializes a Clue board.

        Raises a ValueError if the board_path has issues.

        str board_path: path to Clue board .csv file.
        """
        # game state
        self.board = None

        # game details
        self.weapons = None
        self.suspects = None
        self.rooms = None

        self.suspect_locations = {}

        # populate game state and details
        self.read_board_weapons(board_path)
        self.populate_suspects_rooms()
        self.populate_suspect_locations()

    def populate_suspects_rooms(self):
        """
        Accesses the board and determines the rooms and suspects.

        Populates self.rooms and self.suspects.
        """
        # non room and suspect tiles
        basic_tiles = {DOOR, HALL, WALL}

        self.rooms = set()
        self.suspects = set()

        x_lim = (0, len(self.board[0]))
        y_lim = (0, len(self.board))

        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                # check if tile is a room or suspect
                if tile not in basic_tiles:
                    # suspects are on the edge of the board
                    if x in x_lim or y in y_lim:
                        self.suspects.add(tile)
                    else:
                        self.rooms.add(tile)

    def read_board_weapons(self, board_path):
        """
        Reads a Clue board from a .csv file.

        Populates self.board and self.weapons.

        Raises a ValueError if the board_path has issues.

        str board_path: path to Clue board .csv file.
        """
        try:
            with open(board_path, "r") as f:
                # read weapons from first row
                self.weapons = f.readline().strip().split(",")
                # read board from remaining rows
                board = [line.strip().split(",") for line in f]
                if not board:  # check if the board is empty
                    raise ValueError("The CSV file is empty.")
                self.board = board
        except FileNotFoundError:
            print(f"Error: The file {board_path} does not exist.")
        except ValueError as ve:
            print(ve)

        raise ValueError("The board could not be read.")
