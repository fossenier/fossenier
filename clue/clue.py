import os
import sys

from random import randint
from typing import List

BOARD_FILE = "board.csv"
PLAYERS = 6


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


def main():
    # gets lists of suspects, weapons, and rooms from the board file
    suspects, weapons, rooms = read_board()

    suspects = CardStack(suspects)
    weapons = CardStack(weapons)
    rooms = CardStack(rooms)

    murderer = suspects.draw_card() + weapons.draw_card() + rooms.draw_card()
    clue_deck = suspects + weapons + rooms

    # TODO remove after testing
    print("Suspects:", suspects)
    print("Weapons:", weapons)
    print("Rooms:", rooms)
    print("Murderer:", murderer)

    player_hands = []
    player_hand_size = len(clue_deck) // PLAYERS

    for _ in range(PLAYERS):
        player_hand = CardStack()
        for _ in range(player_hand_size):
            player_hand = player_hand + clue_deck.draw_card()
        # TODO remove
        print(player_hand)
        player_hands.append(player_hand)

    # TODO remove
    print(clue_deck)


def pick_murderer(
    suspects: List[str], weapons: List[str], rooms: List[str]
) -> List[str]:
    """
    Purpose:
        Picks a random murderer (suspect, weapon, and room) from the provided card stacks.
    Pre-conditions:
        suspects List[str]: The suspect cards.
        weapons List[str]: The weapon cards.
        rooms List[str]: The room cards.
    Post-conditions:
        Modifies the initial lists by removing a card from each
    Returns:
        List[str]: A random suspect, weapon, and room card.
    """
    if len(suspects) == 0 or len(weapons) == 0 or len(rooms) == 0:
        raise ValueError("Error: must provide non-empty lists")

    # pick the murderer, weapon, and location
    murderer = []
    for stack in (suspects, weapons, rooms):
        murderer.append(stack.pop(randint(0, len(stack) - 1)))
    return murderer


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
