import random as r


def gen_dice():
    dice = []
    for i in range(6):
        rolls = []
        for i in range(4):
            rolls.append(r.randint(1, 6))
        rolls.remove(min(rolls))
        dice.append(sum(rolls))
    return dice


def check_ranger(dice):
    dice = sorted(gen_dice())
    required_rolls = [12, 13, 14, 14]
    for roll in required_rolls:
        if dice.pop() < required_rolls.pop():
            return False
    return True


def sim():
    sims = 1000000
    true = 0
    for i in range(sims):
        true += 1 if check_ranger(gen_dice()) else 0

    print(true / sims * 100)


sim()
