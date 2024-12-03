from typing import List

from treasure_starter import read_data


def steal(treasures: List[str], room: int, i: int = 0) -> int:
    if room <= 0 or i >= len(treasures):
        return 0

    treasure = treasures[i]
    # Don't take
    val1 = steal(treasures, room, i + 1)

    # Take (if there's enough room)
    val2 = 0
    if room >= treasure[1]:
        val2 = steal(treasures, room - treasure[1], i + 1) + treasure[0]

    return max(val1, val2)


def main():
    treasures = [(entry["value"], entry["weight"]) for entry in read_data("room3.txt")]
    best = steal(treasures, 300)
    print(best)


if __name__ == "__main__":
    main()
