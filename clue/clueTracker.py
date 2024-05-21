class ClueTracker:
    """
    This object will allow a player to keep track of the information provided
    throughout the game, and make deductions about the unknown cards.
    """

    def __init__(self, players, suspects, weapons, rooms, hand, cpu_suspect):
        self.cards = suspects + weapons + rooms
        self.links = []
        self.players = players
        self.rooms = rooms
        self.suspects = suspects
        self.tally_sheet = {
            player: {card: None for card in self.cards} for player in players
        }
        self.weapons = weapons

        murderer_cards = 3
        self.hand_size = (
            (len(self.cards) - murderer_cards) // len(players) if len(players) else 0
        )
        for card in hand:
            self.store_revealed_card(cpu_suspect, card)

    def calculate_probabilities(self):
        """
        Purpose:
            Check if there are less than 5 final accusations possible and determine their likelyhood.
        Pre-conditions:
            None.
        Post-conditions:
            None.
        Returns:
            List[List[str], int: a list of possible final accusations and the likelyhood
            of this accusation (number of times false appears on the sheets).
            None: if there are more than 5 possible final accusations.
        """

        def find_all_false(items):
            return [
                item
                for item in items
                if all(
                    self.tally_sheet[player][item] == False for player in self.players
                )
            ]

        self.update_tally_sheet()
        # find all rooms, suspects, and weapons that all players have marked as false
        false_rooms = find_all_false(self.rooms)
        false_suspects = find_all_false(self.suspects)
        false_weapons = find_all_false(self.weapons)

        # there are more than 5 possible final accusations
        if len(false_rooms) * len(false_suspects) * len(false_weapons) > 5:
            return None

        possible_final_accusations = []
        for room in false_rooms:
            for suspect in false_suspects:
                for weapon in false_weapons:
                    possible_final_accusations.append(
                        [suspect, weapon, room],
                        self.count_false(room)
                        + self.count_false(suspect)
                        + self.count_false(weapon),
                    )
        return possible_final_accusations

    def count_false(self, item):
        return sum(self.tally_sheet[player][item] == False for player in self.players)

    def is_true(self, item):
        for player in self.players:
            if self.tally_sheet[player][item]:
                return True
        return False

    def draw_sheet(self, filename):
        from PIL import Image, ImageDraw, ImageFont

        self.update_tally_sheet()

        def get_tile_color(tile):
            tile_colors = {
                True: (211, 174, 141),  # light brown for True
                False: (244, 91, 96),  # soft red for False
                None: (238, 228, 210),  # light cream for Unknown
            }
            return tile_colors.get(
                tile, (255, 255, 0)
            )  # fallback to red (shouldn't be used)

        cell_size = 60
        cell_border = 5
        header_size = 120

        # set the width and height based on the number of players and cards
        width = len(self.players) * cell_size + header_size
        height = len(self.cards) * cell_size + header_size

        img = Image.new("RGBA", (width, height), (40, 39, 41))  # dark gray background
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # drawing headers (players as columns, cards as rows)
        # ChatGPT wrote this, I don't understand it
        for i, player in enumerate(self.players):
            player_position = (header_size + (i + 0.5) * cell_size, header_size / 2)
            draw.text(player_position, player, font=font, anchor="mm", fill="white")
        for j, card in enumerate(self.cards):
            card_position = (header_size / 2, header_size + (j + 0.5) * cell_size)
            draw.text(card_position, card, font=font, anchor="mm", fill="white")

        # draw rows one at a time (there are always more cards than players and thus rows than columns)
        for row, card in enumerate(self.cards):
            # look at each player's information for the row
            for col, player in enumerate(self.players):
                information = self.tally_sheet[player][card]
                tile_fill = get_tile_color(information)

                # where to start filling in the coloured tile
                tile_top_left = (
                    header_size + col * cell_size + cell_border,
                    header_size + row * cell_size + cell_border,
                )
                # where to stop filling in the coloured tile
                tile_bottom_right = (
                    header_size + (col + 1) * cell_size - cell_border,
                    header_size + (row + 1) * cell_size - cell_border,
                )

                draw.rectangle([tile_top_left, tile_bottom_right], fill=tile_fill)

        img.save(filename)
        print(f"Tally sheet drawn and saved as {filename}")

    def store_accusation(self, suspect, weapon, room, responder, response):
        """
        Purpose:
            Records all information generated by an accusation.
        Pre-conditions:
            str suspect: the accused suspect.
            str weapon: the accused weapon.
            str room: the accused room.
            str responder: the player responding to the accusation.
            str response: the response to the accusation. "y" for yes, "n" for no.
        Post-conditions:
            self.tally_sheet: the tally sheet may be updated with the new information.
            self.links: a new link may be added if the response is positive.
        Returns:
            None.
        """
        if response not in ["y", "n"]:
            raise ValueError("Response must be 'y' for yes or 'n' for no")

        # create a link on the cards if the response is positive
        if response == "y":
            self.links.append((responder, [suspect, weapon, room]))
        # mark all cards as false if the response is negative
        elif response == "n":
            for card in [suspect, weapon, room]:
                if card in self.cards:
                    self.tally_sheet[responder][card] = False

    def store_revealed_card(self, player, card):
        """
        Purpose:
            Record when a card is explicitly revealed to you.
        Pre-conditions:
            str player: the player who revealed the card.
            str item: the card that was revealed.
        Post-conditions:
            self.tally_sheet: the tally sheet is updated with the new information.
        Returns:
            None.
        """
        if player not in self.players or card not in self.cards:
            raise ValueError("Invalid player or card")
        self.tally_sheet[player][card] = True

    def update_tally_sheet(self):
        """
        Purpose:
            Make as many deductions as possible based on the current information.
        Pre-conditions:
            None.
        Post-conditions:
            self.tally_sheet: the tally sheet is updated with new information.
        Returns:
            None.
        """
        changes_made = True
        while changes_made:
            changes_made = (
                self.__check_full_hands()
                or self.__check_found_cards()
                or self.__resolve_links()
            )

    def __check_found_cards(self):
        """
        Purpose:
            When a card is known to be in a hand, nobody else is holding it.
        Pre-conditions:
            None.
        Post-conditions:
            self.tally_sheet: the tally sheet is updated with new information.
        Returns:
            bool: True if changes were made, False otherwise.
        """
        changes_made = False
        for card in self.cards:
            owners = [
                player
                for player, cards in self.tally_sheet.items()
                if cards[card] is True
            ]
            if len(owners) == 1:
                for player in self.players:
                    if player not in owners and self.tally_sheet[player][card] is None:
                        self.tally_sheet[player][card] = False
                        changes_made = True
        return changes_made

    def __check_full_hands(self):
        """
        Purpose:
            When a player's whole hand is known, mark the other cards as false.
        Pre-conditions:
            None.
        Post-conditions:
            self.tally_sheet: the tally sheet is updated with new information.
        Returns:
            bool: True if changes were made, False otherwise.
        """
        changes_made = False
        for player, player_cards in self.tally_sheet.items():
            if list(player_cards.values()).count(True) == self.hand_size:
                for card, value in player_cards.items():
                    if value is None:
                        self.tally_sheet[player][card] = False
                        changes_made = True
        return changes_made

    def __resolve_links(self):
        """
        Purpose:
            Resolve links using deduction. If a player does NOT have two cards, they have the third.
        Pre-conditions:
            None.
        Post-conditions:
            self.tally_sheet: the tally sheet is updated with new information.
        Returns:
            bool: True if links were resolved, False otherwise.
        """
        changes_made = False
        updated_links = []
        for link in self.links:
            responder, linked_cards = link
            known_cards = [
                card
                for card in linked_cards
                if any(
                    self.tally_sheet[player][card] == True for player in self.players
                )
            ]

            if len(known_cards) == len(linked_cards) - 1:
                unknown_card = next(
                    card for card in linked_cards if card not in known_cards
                )
                if self.tally_sheet[responder][unknown_card] is None:
                    self.tally_sheet[responder][unknown_card] = True
                    changes_made = True
            else:
                updated_links.append(link)

        self.links = updated_links
        return changes_made
