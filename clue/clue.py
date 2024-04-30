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


def main():
    game = Clue("board.csv")


if __name__ == "__main__":
    main()
