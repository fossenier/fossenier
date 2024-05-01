"""
This is a second slice of Clue that is focused on simply giving instructions.
"""


class ClueTracker:
    def __init__(self, players, suspects, weapons, rooms):
        self.players = players
        self.items = suspects + weapons + rooms
        # Initialize the tally sheet with None (unknown)
        self.tally_sheet = {
            player: {item: None for item in self.items} for player in players
        }
        self.links = []

    def mark_accusation(self, accuser, suspect, weapon, room, responder, response):
        # Create a link if the response is positive
        if response == "yes":
            self.links.append((responder, {suspect, weapon, room}))
        # Mark all as false if the response is negative
        elif response == "no":
            for item in [suspect, weapon, room]:
                self.tally_sheet[responder][item] = False
        self.process_cyclical_checks()

    def reveal_card(self, player, item):
        # Mark an item as true for a player
        self.tally_sheet[player][item] = True
        self.process_cyclical_checks()

    def process_cyclical_checks(self):
        changes = True
        while changes:
            changes = False
            # Rule 1: All cards known for a player
            for player, items in self.tally_sheet.items():
                if list(items.values()).count(True) == self.player_card_count(player):
                    for item, value in items.items():
                        if value is None:
                            self.tally_sheet[player][item] = False
                            changes = True
            # Rule 2: Item known to belong to one player
            for item in self.items:
                true_owners = [
                    p for p, v in self.tally_sheet.items() if v[item] is True
                ]
                if len(true_owners) == 1:
                    for player in self.players:
                        if (
                            player not in true_owners
                            and self.tally_sheet[player][item] is None
                        ):
                            self.tally_sheet[player][item] = False
                            changes = True
            # Resolve links
            for link in self.links:
                responder, items = link
                known_items = [
                    i
                    for i in items
                    if any(self.tally_sheet[p][i] is True for p in self.players)
                ]
                if len(known_items) == len(items) - 1:
                    unknown_item = list(items - set(known_items))[0]
                    self.tally_sheet[responder][unknown_item] = True
                    changes = True
            self.links = [
                link for link in self.links if not self.is_link_resolved(link)
            ]

    def is_link_resolved(self, link):
        responder, items = link
        return all(self.tally_sheet[responder][item] is not None for item in items)

    def player_card_count(self, player):
        # This needs to be defined or known externally
        return 3  # Example: Every player has 3 cards


class Clue(object):
    def __init__(self, game_path):
        self.board = []  # the game board
        self.cpu_location = (None, None)  # the CPU location
        self.cpu_suspect = None  # the CPU suspect
        self.rooms = []  # list of room names
        self.suspects = {}  # key: suspect name, value: (x, y) starting position
        self.suspect_order = []  # the order of the players
        self.weapons = []  # list of weapon names

        self.__read_board_data(game_path)

    def initialize_game(self):
        """
        Purpose:
            Initializes the game with the two required user inputs before the main loop.
        Pre-conditions:
            None.
        Post-conditions:
            self.suspect_order, self.cpu_suspect, self.cpu_location are populated.
        Returns:
            None.
        """
        print("Welcome to Clue!")
        self.__prompt_game_order()
        self.__prompt_cpu_suspect()
        self.cpu_location = self.suspects[self.cpu_suspect]

    def run_game(self):
        """
        Purpose:
            The main loop of the game. Handles CPU and player turns until a final
            accusation on the part of the CPU is made.
        """
        accusation_made = False
        while not accusation_made:
            # run through the player order
            for player in self.suspect_order:
                # handle human turns
                if player != self.cpu_suspect:
                    self.__human_turn(player)
                # handle CPU turn
                else:
                    accusation_made = self.__cpu_turn()

    def __cpu_turn(self):
        print("CPU turn not implemented.")

    def __get_attribute_name(self, provided_attribute, attributes):
        """
        Purpose:
            Get the attribute name from a list of attributes.
        Pre-conditions:
            str provided_attribute: the attribute to find.
            list attributes: the list of attributes to search.
        Post-conditions:
            None.
        Returns:
            str: the attribute name.
        """
        # search for the attribute in the list of attributes
        for attribute in attributes:
            if provided_attribute.lower() in attribute.lower():
                return attribute

    def __get_next_player(self, current_player):
        """
        Purpose:
            Get the next player in the order of play.
        Pre-conditions:
            str current_player: the current player.
        Post-conditions:
            None.
        Returns:
            str: the next player.
        """
        current_index = self.suspect_order.index(current_player)
        return self.suspect_order[(current_index + 1) % len(self.suspect_order)]

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

    def __human_turn(self, player):
        room, weapon, suspect = self.__prompt_human_accusation(player)

        is_card_revealed = "n"
        accused_player = self.__get_next_player(player)
        while is_card_revealed != "y":
            # nobody revealed a card
            if accused_player == player:
                return

            # note if the accused player revealed a card
            is_card_revealed = input(
                f"Did {accused_player} reveal a card to {player} (y/n)? "
            ).lower()
            accused_player = self.__get_next_player(accused_player)

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
            entered_cpu = input(f"Enter the CPU suspect({self.suspect_order}): ")
            cpu_suspect = self.__get_attribute_name(entered_cpu, self.suspect_order)

        # save to the object the suspect as named in self.suspect_order
        self.cpu_suspect = self.__get_attribute_name(cpu_suspect, self.suspect_order)

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
                validated_suspect = self.__get_attribute_name(
                    user_suspect, actual_suspects
                )
                validated_suspects.append(validated_suspect)
                actual_suspects.remove(validated_suspect)

            # make sure 2 or more players are in the game
            if len(validated_suspects) < 2:
                print(
                    f"Error: you must have at least 2 valid players. You entered {validated_suspects}."
                )
                continue

            # use the validated order
            self.suspect_order = validated_suspects
            is_valid_order = True

    def __prompt_human_accusation(self, player):
        room, weapon, suspect = None, None, None
        while True:
            accusation = [
                info.strip()
                for info in input(f"{player} accused (room, weapon, suspect): ").split(
                    ","
                )
            ]
            room = self.__get_attribute_name(accusation[0], self.rooms)
            weapon = self.__get_attribute_name(accusation[1], self.weapons)
            suspect = self.__get_attribute_name(accusation[2], self.suspects.keys())

            if not room or not weapon or not suspect:
                print("Error: invalid accusation. Please try again.")
                continue
            break

        return room, weapon, suspect

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
