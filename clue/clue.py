"""
This is a second slice of Clue that is focused on simply giving instructions.
"""

from clueTracker import ClueTracker


class Clue(object):
    # TODO handle players ending in hallway
    def __init__(self, game_path):
        self.board = []  # the game board
        self.cpu_location = (None, None)  # the CPU location
        self.cpu_suspect = None  # the CPU suspect
        self.rooms = []  # list of room names
        self.suspects = {}  # key: suspect name, value: (x, y) starting position
        self.suspect_order = []  # the order of the players
        self.tallysheet = None  # the clue tracker
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
        cpu_cards = self.__prompt_cpu_cards()
        self.cpu_location = self.suspects[self.cpu_suspect]
        self.tallysheet = ClueTracker(
            self.suspect_order.copy(),
            list(self.suspects.keys()).copy(),
            self.weapons.copy(),
            self.rooms.copy(),
            cpu_cards,
            self.cpu_suspect,
        )

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
                self.tallysheet.draw_sheet("tallysheet.png")
                # handle human turns
                if player != self.cpu_suspect:
                    self.__human_turn(player)
                # handle CPU turn
                else:
                    accusation_made = self.__cpu_turn()

    def __cpu_turn(self):
        def best_item(items):
            """
            Purpose:
                Get the item with the most false marks.
            Pre-conditions:
                str item: the item to find.
                list items: the list of items to search.
            Post-conditions:
                None.
            Returns:
                str: the best item.
            """
            best_item = [None, float("-inf")]
            for item in items:
                # don't ask about known items
                if self.tallysheet.is_true(item):
                    continue
                # ask about items most likely to be false
                score = self.tallysheet.count_false(item)
                if score > best_item[1]:
                    best_item = [item, score]
            return best_item[0]

        # determine if final accusation should be made
        outcomes = self.tallysheet.calculate_probabilities()
        # there is a 1 in 5 chance of success on accusing
        if outcomes:
            best_outcome = [[], 0]
            for outcome in outcomes:
                if outcome[1] > best_outcome[1]:
                    best_outcome = outcome
            # the number of times false is marked for a 100% chance of success
            guaranteed_accusation = len(self.suspect_order) * 3
            if best_outcome[1] / guaranteed_accusation > 0.8:
                print(f"CPU makes final accusation {best_outcome[0]}.")
                return

        # get roll
        movement = self.__prompt_dice_roll(self.cpu_suspect)

        # get possible moves
        possible_moves = self.__possible_moves(movement)

        # determine best weapon and suspect
        weapon = best_item(self.weapons)
        suspect = best_item(list(self.suspects.keys()))

        # determine best room
        room = best_item([move[0] for move in possible_moves])
        chosen_room = None

        # all rooms are known
        if not room:
            # go as far as possible (to explore more rooms next turn)
            furthest_room = [None, 0]
            for move in possible_moves:
                if move[1] > furthest_room[1]:
                    furthest_room = move
            chosen_room = furthest_room[0]
        # a room is not known
        else:
            chosen_room = room

        # move
        self.cpu_location = self.__get_tile_position(chosen_room)

        # end turn if the CPU is in a hall

        # make accusation
        print(f"CPU accuses {suspect}, {weapon}, {chosen_room}.")

        is_card_revealed = "n"
        questioned_player = self.__get_next_player(self.cpu_suspect)
        while is_card_revealed != "y":
            # no players could reveal a card and the accusation looped back to the cpu
            if questioned_player == self.cpu_suspect:
                return

            # note if the accused player revealed a card
            is_card_revealed = None
            while is_card_revealed not in ["y", "n", "skip"]:
                is_card_revealed = input(
                    f"Did {questioned_player} reveal a card to you (y/n)? "
                ).lower()

            if is_card_revealed == "skip":
                return

            if is_card_revealed == "n":
                self.tallysheet.store_accusation(
                    suspect, weapon, room, questioned_player, is_card_revealed
                )
            else:
                revealed_card = self.__get_attribute_name(
                    input(f"Enter the card {questioned_player} revealed: "),
                    list(self.suspects.keys()) + self.weapons + self.rooms,
                )
                self.tallysheet.store_revealed_card(questioned_player, revealed_card)
            questioned_player = self.__get_next_player(questioned_player)

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

    def __hand_size(self):
        """
        Purpose:
            Get the size of each player's hand.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        Returns:
            int: the size of each player's hand.
        """
        cards_set_aside_for_murderer = 3
        return (
            len(self.suspects)
            + len(self.weapons)
            + len(self.rooms)
            - cards_set_aside_for_murderer
        ) // len(self.suspect_order)

    def __human_turn(self, player):
        room, weapon, suspect = self.__prompt_human_accusation(player)

        is_card_revealed = "n"
        questioned_player = self.__get_next_player(player)
        while is_card_revealed != "y":
            # no players could reveal a card and the accusation looped back to the accuser
            if questioned_player == player:
                return

            # note if the accused player revealed a card
            is_card_revealed = None
            while is_card_revealed not in ["y", "n", "skip"]:
                is_card_revealed = input(
                    f"Did {questioned_player} reveal a card to you (y/n)? "
                ).lower()

            if is_card_revealed == "skip":
                return

            is_card_revealed = input(
                f"Did {questioned_player} reveal a card to {player} (y/n)? "
            ).lower()
            self.tallysheet.store_accusation(
                suspect, weapon, room, questioned_player, is_card_revealed
            )
            questioned_player = self.__get_next_player(questioned_player)

    def __possible_moves(self, movement):
        """
        Purpose:
            Determines all possible rooms the CPU can move to and their distances.
        Pre-conditions:
            int movement: the number of spaces the CPU can move.
        Post-conditions:
            None.
        Returns:
            list of tuples (str, int): Each tuple contains a room and its distance from the start.
        """
        # the four possible moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def is_within_bounds(position, grid=self.board):
            """
            Check if the position is within the board boundaries to prevent indexing errors.
            """
            x, y = position
            return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

        def enter_door(position):
            """
            Purpose:
                Enter a door.
            Pre-conditions:
                tuple position: the position of the door.
            Post-conditions:
                None.
            Returns:
                str: the room the door leads to.
            """
            room = None
            not_room = [" ", "x", "Door"]
            x_coord, y_coord = position
            for direction in directions:
                neighbor = (x_coord + direction[0], y_coord + direction[1])
                # Check bounds before accessing the board to avoid index errors
                if (
                    is_within_bounds(neighbor)
                    and self.board[neighbor[1]][neighbor[0]] not in not_room
                ):
                    room = self.board[neighbor[1]][neighbor[0]]
            return room

        # the cpu starts in a room, so needs to first step out into the nearest "Door" which is the hall
        starting_location = self.cpu_location
        if self.board[self.cpu_location[1]][self.cpu_location[0]] in self.rooms:
            for direction in directions:
                neighbor = (
                    self.cpu_location[0] + direction[0],
                    self.cpu_location[1] + direction[1],
                )
                # Ensure neighbor is within bounds before checking for "Door"
                if (
                    is_within_bounds(neighbor)
                    and self.board[neighbor[1]][neighbor[0]] == "Door"
                ):
                    starting_location = neighbor

        # initialize the queue for breadth-first search
        exploration_queue = [
            (starting_location, 0)
        ]  # Each entry is (position, distance)
        board_width = len(self.board[0])
        board_height = len(self.board)
        visited = [[False for _ in range(board_width)] for _ in range(board_height)]

        # store eligible rooms
        rooms = []
        while exploration_queue:
            current_position, current_distance = exploration_queue.pop(0)

            # check if the player can enter a door
            tile = self.board[current_position[1]][current_position[0]]
            distance_to_enter_room = current_distance + 1
            if tile == "Door" and distance_to_enter_room <= movement:
                room = enter_door(current_position)
                if room:
                    rooms.append((room, current_distance))
                else:
                    raise ValueError("Error: door leads to no room.")

            # explore neighbors
            for direction in directions:
                neighbor = (
                    current_position[0] + direction[0],
                    current_position[1] + direction[1],
                )

                # check board boundaries and if the neighbor is walkable and not visited
                if (
                    is_within_bounds(neighbor, visited)
                    and not visited[neighbor[1]][neighbor[0]]
                    and self.board[neighbor[1]][neighbor[0]] != "x"
                ):
                    exploration_queue.append((neighbor, current_distance + 1))
                    visited[neighbor[1]][neighbor[0]] = True

        return rooms

    def __prompt_cpu_cards(self):
        """
        Purpose:
            Prompts the user to enter the cards the CPU has.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        Returns:
            List[str]: the cards the CPU has.
        """
        # get the cards from user
        cpu_cards = []
        hand_size = self.__hand_size()
        while len(cpu_cards) < hand_size:
            card = input(f"Enter the card the CPU has ({len(cpu_cards) + 1}): ")
            card = self.__get_attribute_name(
                card, list(self.suspects.keys()) + self.weapons + self.rooms
            )
            if card and card not in cpu_cards:
                cpu_cards.append(card)
            else:
                print("Error: card already entered. Please enter a new card.")
        return cpu_cards

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

    def __prompt_dice_roll(self, player):
        """
        Purpose:
            Prompts the user to input the dice roll.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        Returns:
            int: the dice roll.
        """
        dice_roll = 0
        while dice_roll < 2 or dice_roll > 12:
            raw_dice_roll = input(f"Enter the dice roll for {player}: ")
            if raw_dice_roll.isdigit():
                dice_roll = int(raw_dice_roll)
            else:
                print("Error: invalid dice roll. Please try again.")
        return dice_roll

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

        with open(game_path, "r") as f:
            # skip weapon config
            f.readline()
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
