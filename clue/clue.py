import os
import sys
from typing import List

BOARD_FILE = "board.csv"


def main():
    results = read_board()
    print(results)


def read_board(provided_path: str = BOARD_FILE) -> List[List[str]]:
    """
    Purpose:
         Reads a clue game configuration file to extract the names of suspects, weapons, and rooms.

     Pre-conditions:
        provided_path str:
        The path to the file containing the clue game configuration. If None, a default path is used.
        The file should contain 6 lines, with the first 3 lines being comments and the last 3 lines
        containing comma-separated values representing suspects, weapons, and rooms.

     Post-conditions:
         The function will terminate the program if the specified file does not exist.

     Returns:
         List[str]: The suspects.
         List[str]: The weapons.
         List[str]: The rooms.
    """
    path = provided_path if provided_path else BOARD_FILE

    if not os.path.exists(path):
        print(f"Error: {path} not found")
        sys.exit(1)

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

    return suspects, weapons, rooms


if __name__ == "__main__":
    main()
