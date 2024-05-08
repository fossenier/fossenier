"""
This is a third slice of Clue.
It directs the player like a puppet to play the game.
"""

from config import BOARD_PATH

from board import Board
from detective_notes import DetectiveNotes
from user_interface import UI


class ClueAlgorithm(object):
    def __init__(self, board_path):
        # read in board
        self.board = Board(board_path)

        self.notes = DetectiveNotes()
        self.ui = UI()

        #

    def test(self):
        print(self.notes.test)
        print(self.ui.test)


def main():
    algorithm = ClueAlgorithm(BOARD_PATH)
    algorithm.test()


if __name__ == "__main__":
    main()
