"""
This is a third slice of Clue.
It directs the player like a puppet to play the game.
"""

from board import Board
from detective_notes import DetectiveNotes
from user_interface import UI


class ClueAlgorithm(object):
    def __init__(self):
        self.board = Board()
        self.notes = DetectiveNotes()
        self.ui = UI()

    def test(self):
        print(self.board.test)
        print(self.notes.test)
        print(self.ui.test)


def main():
    algorithm = ClueAlgorithm()
    algorithm.test()


if __name__ == "__main__":
    main()
