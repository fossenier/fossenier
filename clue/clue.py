"""
This is a second slice of Clue that is focused on simply giving instructions.
"""


class Clue:
    def __init__(self):
        self.ROOMS = [
            "Ballroom",
            "Billiard Room",
            "Conservatory",
            "Dining Room",
            "Hall",
            "Kitchen",
            "Library",
            "Lounge",
            "Study",
        ]
        self.SUSPECTS = [
            "Colonel Mustard",
            "Miss Scarlet",
            "Mr. Green",
            "Mrs. Peacock",
            "Mrs, White",
            "Professor Plum",
        ]
        self.WEAPONS = [
            "Candlestick",
            "Knife",
            "Lead Pipe",
            "Revolver",
            "Rope",
            "Wrench",
        ]
        self.suspect_order = []
        self.cpu_suspect = None


def main():
    pass


if __name__ == "__main__":
    main()
