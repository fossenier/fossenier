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
        self.distance_travelled = 0
        self.track_length = track_length
        self.value = 0
        self.killed = False

    def advance(self) -> bool:
        self.distance_travelled += 1
        return self.distance_travelled >= self.track_length

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

    def earn(self, value) -> None:
        # We assume this value to be an exact multiple
        self.coins += value // COIN_VALUE


class Player:
    def __init__(self, hand) -> None:
        self.hand: List[int] = hand
        self.wallet = Wallet()
        self.eliminated = False

    def redeal(self, hand) -> None:
        self.hand = hand

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

    def pay(self, value) -> int:
        (solvent, payment) = self.wallet.pay(value)
        if not solvent:
            self.eliminated = True
        return payment

    def horse_count(self, card) -> int:
        return self.hand.count(card)

    def payout(self, card, value) -> None:
        for _ in range(self.hand.count(card)):
            self.wallet.earn(value)


def main():
    board = Board()
    deck = Deck()
    players = [Player([]) for _ in range(PLAYER_COUNT)]
    dealer = 0
    assert PLAYER_COUNT >= 2

    round_pot_carryover = 0

    # TODO make this a while loop until eliminations
    game_over = False
    while not game_over:
        # Current players
        active_players = len(players)

        round_pot = round_pot_carryover
        # Deal out hands for each player
        hands = deck.deal(active_players)
        for i in range(active_players):
            players[i].redeal(hands[i])

        # First player
        active_player = (dealer + 1) % active_players

        # Kill horses
        horse_kills = 0
        while horse_kills < 4:
            # Perform 2d6 roll
            roll = random.randint(1, 6) + random.randint(1, 6)
            # The horse is alive, kill it from all hands
            if not board.horses[roll].killed:
                # Kill values are 5, 10, 15, 20
                kill_value = COIN_VALUE * (horse_kills + 1)
                # Set the horse to be killed
                board.horses[roll].kill(kill_value)
                horse_kills += 1
                # Kill this horse for each player
                for player in players:
                    # See what they chip in to the pot
                    pot_addition = player.kill(roll, kill_value)
                    round_pot += pot_addition
                    # Track eliminations
                    if player.eliminated:
                        players.remove(player)
                        active_players -= 1
                        if active_players == 1:
                            game_over = True
                            break
                if game_over:
                    break
            # The horse is dead, active player pays for the roll
            else:
                pot_addition = players[active_player].pay(board.horses[roll].value)
                round_pot += pot_addition
                # Track eliminations
                if players[active_player].eliminated:
                    players.pop(active_player)
                    active_players -= 1
                    if active_players == 1:
                        game_over = True
                        break
            if game_over:
                break
            # Update the current player
            active_player = (active_player + 1) % active_players
        if game_over:
            break

        round_over = False
        winning_horse = None
        while not round_over:
            roll = random.randint(1, 6) + random.randint(1, 6)
            if board.horses[roll].killed:
                pot_addition = players[active_player].pay(board.horses[roll].value)
                round_pot += pot_addition
                # Track eliminations
                if players[active_player].eliminated:
                    players.pop(active_player)
                    active_players -= 1
                    if active_players == 0:
                        game_over = True
                        break
            else:
                round_over = board.horses[roll].advance()
                winning_horse = roll
            if game_over:
                break
            # Advance to the next player
            active_player = (active_player + 1) % active_players
        if game_over:
            break

        # Pay out the pot
        coins = round_pot // COIN_VALUE
        # Count how many of the winning horse is in hands (because sometimes
        # a person will be eliminated before collecting on a winning horse)
        winning_horses = sum(player.horse_count(winning_horse) for player in players)
        if winning_horses == 0:
            round_pot_carryover = coins * COIN_VALUE
        else:
            # Payouts must be equal, based on how many winning horses are in hands (usually 4)
            round_pot_carryover = (coins % winning_horses) * COIN_VALUE
            payout_value = (coins // winning_horses) * COIN_VALUE

            # Payout players, those who have the horse
            for player in players:
                player.payout(winning_horse, payout_value)

        dealer = (dealer + 1) % active_players
        board.reset()
        deck.shuffle()

    print(players[0].wallet.coins)
    print(len(players))


if __name__ == "__main__":
    main()
