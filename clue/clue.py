import os
import sys

from random import randint
from typing import List

BOARD_FILE = "board.csv"
PLAYERS = 6


class MurderInfo(object):
    """
    What a player knows about the murderer.
    """

    def __init__(self, suspects: "CardStack", weapons: "CardStack", rooms: "CardStack"):
        """
        Every player in the game keeps track of whether or not another given player
        has"""
        self.__info = {}
        # for each player
        for player in range(PLAYERS):
            info_about_player = {}
            # mark that each suspect, weapon, and room is unknown
            for info_type in (suspects, weapons, rooms):
                for info in info_type:
                    info_about_player[info] = False


class Guess(object):
    """
    Represents a guess made by a player.
    """

    def __init__(
        self,
        suspect: "CardStack",
        weapon: "CardStack",
        room: "CardStack",
        respondant: "Player",
        response: "CardStack",
    ):
        self.__suspect = suspect
        self.__weapon = weapon
        self.__room = room
        self.__respondant = respondant
        self.__response = response

    def __str__(self):
        """
        Returns a string representation of the guess.
        """
        return f"Guess: {self.__suspect}, {self.__weapon}, {self.__room}"


class Player(object):
    """
    Represents a player in the game of Clue.
    """

    def __init__(
        self,
        hand: List[str],
        suspects: "CardStack",
        weapons: "CardStack",
        rooms: "CardStack",
    ):
        self.__hand = CardStack(hand)
        self.__info = MurderInfo(suspects, weapons, rooms)
        self.__guessses = []

    def pickup(self, stack: "CardStack"):
        """
        Adds a card to the player's hand.
        """
        self.__hand = self.__hand + stack

    def ask(self, question: "Guess"):
        """
        Track a guess made by the player.
        """
        self.__guessses.append(question)

    def __str__(self):
        """
        Returns a string representation of the player's hand.
        """
        return f"Hand: {str(self.__hand)}"


class CardStack(object):
    """
    Treats a list of strings as a stack of cards.
    """

    def __init__(self, cards: List[str] = []):
        self.__cards = cards

    def __len__(self):
        """
        Returns the number of cards in the stack.
        """
        return len(self.__cards)

    def draw_card(self):
        """
        Removes a card from the stack and returns it as a new stack.
        """
        drawn_card = self.__cards.pop(randint(0, len(self.__cards) - 1))
        return CardStack([drawn_card])

    def __add__(self, other):
        """
        Shuffles together two stacks of cards.
        """
        return CardStack(self.__cards + other.__cards)

    def __str__(self):
        """
        Returns a string representation of the stack of cards.
        """
        return str(self.__cards)

    def __iter__(self):
        """
        Returns an iterator for the stack of cards.
        """
        return iter(self.__cards)


def main():
    # gets lists of suspects, weapons, and rooms from the board file
    suspects, weapons, rooms = read_board()

    suspects = CardStack(suspects)
    weapons = CardStack(weapons)
    rooms = CardStack(rooms)

    # randomly picks the murderer for the round
    murderer = suspects.draw_card() + weapons.draw_card() + rooms.draw_card()
    # shuffles together the deck players draw hands from
    clue_deck = suspects + weapons + rooms

    # draw all player hands
    players = [Player() for _ in range(PLAYERS)]
    player_hand_size = len(clue_deck) // PLAYERS

    for player in players:
        for _ in range(player_hand_size):
            player.pickup(clue_deck.draw_card())


def read_board(provided_path: str = BOARD_FILE) -> List[List[str]]:
    """
    Purpose:
        Reads a clue game configuration file to extract the card stacks of suspects, weapons, and rooms.
     Pre-conditions:
        provided_path str:
        The path to the file containing the clue game configuration. If None, a default path is used.
        The file should contain 6 lines, with the first 3 lines being comments and the last 3 lines
        containing comma-separated values representing suspects, weapons, and rooms.
     Post-conditions:
        Raises a value error if the path does not exist or if the file format is incorrect.
     Returns:
        List[str]: The suspect cards.
        List[str]: The weapon cards.
        List[str]: The room cards.
    """
    path = provided_path if provided_path else BOARD_FILE

    if not os.path.exists(path):
        raise ValueError(f"Error: {path} not found")

    suspects = []
    weapons = []
    rooms = []

    with open(path, "r") as f:
        # clear the first 3 lines which are simply comments
        for _ in range(3):
            f.readline()

        # read the next 3 lines to extract the suspects, weapons, and rooms
        for input in (suspects, weapons, rooms):
            line = f.readline().strip()
            for item in line.split(","):
                input.append(item)

    if suspects == [""] or weapons == [""] or rooms == [""]:
        raise ValueError(f"Error: {path} does not follow the expected format")

    return [suspects, weapons, rooms]


if __name__ == "__main__":
    main()
