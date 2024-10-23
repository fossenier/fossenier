import random as r


def gen_stats():
    stats = []
    for i in range(6):
        stat = 0
        for i in range(3):
            stat += r.randint(1, 6)
        stats.append(stat)
    return stats


def check_ranger(stats):
    return stats[0] >= 13 and stats[1] >= 12 and stats[2] >= 14 and stats[4] >= 14


def sim():
    sims = 1000000
    true = 0
    for i in range(sims):
        true += 1 if check_ranger(gen_stats()) else 0

    print(true / sims * 100)


sim()
