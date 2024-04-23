"""
This is a first slice of Clue that is hard-coded and manual.
"""

ROOMS = [
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
SUSPECTS = [
    "Colonel Mustard",
    "Miss Scarlet",
    "Mr. Green",
    "Mrs. Peacock",
    "Mrs, White",
    "Professor Plum",
]
WEAPONS = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]


def main():
    output_image("clue_board_1.png")
    # proto_print_board()


def proto_print_board():
    with open("clue_board_1.csv", "r") as f:
        for line in f:
            print(line)


def output_image(filename):
    from PIL import Image, ImageDraw

    cell_size = 50
    cell_border = 2

    # Create a blank canvas
    img = Image.new("RGBA", (50 * cell_size, 50 * cell_size), "black")
    draw = ImageDraw.Draw(img)

    # solution = self.solution[1] if self.solution is not None else None
    # for i, row in enumerate(self.walls):
    #     for j, col in enumerate(row):

    #         # Walls
    #         if col:
    #             fill = (40, 40, 40)

    #         # Start
    #         elif (i, j) == self.start:
    #             fill = (255, 0, 0)

    #         # Goal
    #         elif (i, j) == self.goal:
    #             fill = (0, 171, 28)

    #         # Solution
    #         elif solution is not None and show_solution and (i, j) in solution:
    #             fill = (220, 235, 113)

    #         # Explored
    #         elif solution is not None and show_explored and (i, j) in self.explored:
    #             fill = (212, 97, 85)

    #         # Empty cell
    #         else:
    #             fill = (237, 240, 252)

    #         # Draw cell
    #         draw.rectangle(
    #             (
    #                 [
    #                     (j * cell_size + cell_border, i * cell_size + cell_border),
    #                     (
    #                         (j + 1) * cell_size - cell_border,
    #                         (i + 1) * cell_size - cell_border,
    #                     ),
    #                 ]
    #             ),
    #             fill=fill,
    #         )

    img.save(filename)


if __name__ == "__main__":
    main()
