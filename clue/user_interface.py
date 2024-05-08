"""
This is the inferface for a third slice of Clue.
It handles all communication between the program and the user.
"""


class UI(object):
    def __init__(self):
        self.test = "test"


def main():
    ui = UI()
    print(ui.test)


if __name__ == "__main__":
    main()
