from typing import Dict, List, Tuple
import random


COIN_VALUE = 5
PLAYER_COUNT = 7

# deal cards
# kill horses
# left of dealer starts rolling
# pay, or advance
# divvy out payments
# reset
# deal cards


class Horse:
    def __init__(self, track_length: int) -> None:
        self.track_length = track_length
        self.value = 0
        self.killed = False

    def kill(self, value: int) -> None:
        self.value = value
        self.killed = True

    def reset(self) -> None:
        self.value = 0
        self.killed = False


class Board:
    def __init__(self) -> None:
        self.horses: Dict[int, Horse] = {}

        # [2, 12]
        # [3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3]
        track_length = 3
        for i in range(2, 13):
            self.horses[i] = Horse(track_length)
            if i < 7:
                track_length += 1
            else:
                track_length -= 1

    def reset(self) -> None:
        for v in self.horses.values():
            v.reset()

    def __str__(self) -> str:
        output = ""
        for k, v in self.horses.items():
            output += (
                f"{k:02d}: {v.track_length} | value: {v.value} killed: {v.killed}\n"
            )
        return output


class Deck:
    def __init__(self) -> None:
        self.cards = []
        # 2, 3, 4, ..., 10, J, Q
        for i in range(2, 13):
            # four suits of each card
            for i in range(4):
                self.cards.append(i)

        self.shuffle()

    def deal(self, players: int) -> List[List[int]]:
        hands = [[] for _ in range(players)]

        for i in range(len(self.cards)):
            hands[i % players].append(self.cards[i])

        return hands

    def shuffle(self) -> None:
        random.shuffle(self.cards)


class Wallet:
    def __init__(self) -> None:
        self.coins = 84

    def pay(self, value) -> Tuple[bool, int]:
        # We assume this value to be an exact multiple
        coins = value // COIN_VALUE
        # Enough money, pay the amount
        if self.coins >= coins:
            self.coins -= coins
            return True, value
        # Broke, pay what is left
        else:
            money_left = self.coins * COIN_VALUE
            self.coins = 0
            return False, money_left


class Player:
    def __init__(self, hand) -> None:
        self.hand: List[int] = hand
        self.wallet = Wallet()
        self.eliminated = False

    def kill(self, card, value) -> int:
        pot_addition = 0
        # Kill each horse in this player's hand of the card type
        while card in self.hand:
            self.hand.remove(card)

            # Try and pay for this kill
            (solvent, payment) = self.wallet.pay(value)
            pot_addition += payment
            # Once broke, eliminate this player
            if not solvent:
                self.eliminated = True
                break

        # The amount of money this player pitched in for horse kills
        return pot_addition


def main():
    board = Board()
    deck = Deck()

    for i in range(1):
        # Deal out hands for each player
        hands = deck.deal(PLAYER_COUNT)
        players: List[Player] = []

        # Setup one Player (with money) for each hand
        for hand in hands:
            players.append(Player(hand))

        board.reset()
        deck.shuffle()


if __name__ == "__main__":
    main()
