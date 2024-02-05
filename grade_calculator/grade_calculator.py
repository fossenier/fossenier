"""
Calculates my current weigted average in a university course
"""

import sys


class HandIn:
    """
    Represents a course assignment or hand-in, including its name, weight, and grades.

    Attributes:
        name (str): The name of the hand-in.
        weight (float): The weight of the hand-in as a proportion of the total course grade.
        grades (list of float): A list of grades for this hand-in.
    """

    def __init__(self, name, weight, grades=None):
        self.name = name
        self.weight = weight / 100 if weight > 1 else weight
        self.grades = grades or []

    def average(self):
        """Calculates and returns the average grade for this hand-in."""
        return sum(self.grades) / len(self.grades) if self.grades else 0

    def weighted_average(self):
        """Calculates and returns the weighted average of this hand-in."""
        return self.average() * self.weight

    def is_empty(self):
        """Checks if there are no grades for this hand-in."""
        return len(self.grades) == 0


def main():
    """
    Main function to calculate the current weighted average in a university course.
    It calculates and prints the actual average grade, the average grade with zeroes removed (for incomplete hand-ins),
    and the final grade needed to achieve the desired course average.
    """
    # Get the name of the CSV file containing the course data from the command line
    file_name = get_csv_file()

    # Read course data from the CSV file and initialize variables
    course_name, desired_average, hand_ins = read_csv(file_name)

    actual_average = (
        0  # Initialize the variable to store the actual average of all hand-ins
    )
    zeroes_removed_average = 0  # Initialize the variable for the average with zeroes (incomplete hand-ins) removed
    zeroes_removed_weight = (
        0  # Initialize the total weight of all hand-ins with non-zero grades
    )

    # Calculate the actual average and the zeroes removed average
    for hand_in in hand_ins.values():
        actual_average += (
            hand_in.weighted_average()
        )  # Sum weighted averages for all hand-ins
        if not hand_in.is_empty():  # Exclude hand-ins with no grades
            zeroes_removed_average += (
                hand_in.weighted_average()
            )  # Sum weighted averages for non-empty hand-ins
            zeroes_removed_weight += (
                hand_in.weight
            )  # Sum weights for non-empty hand-ins

    # Adjust the zeroes removed average to reflect the total percentage
    zeroes_removed_average = (
        zeroes_removed_average / zeroes_removed_weight if zeroes_removed_weight else 0
    )

    # Calculate the grade needed on the final to achieve the desired average
    # Default to 0 if there is no final or if the final has no weight
    final_weight = hand_ins.get("final", HandIn("final", 0)).weight
    final_grade_needed = (
        (desired_average - actual_average * 100) / final_weight if final_weight else 0
    )

    # Print out the calculated averages and the required grade for the final exam
    print(f"Current course: {course_name}")
    print(f"Desired average: {desired_average}%")
    print(
        f"Actual average: {actual_average * 100}%"
    )  # Convert actual average to a percentage
    print(
        f"Zeroes removed average: {zeroes_removed_average * 100}%"
    )  # Already in percentage
    print(
        f"Final grade needed: {final_grade_needed}%"
    )  # Required grade on final to achieve desired average


def get_csv_file():
    """
    Gets a vaild csv file from the command line.

    Returns:
        `file_name` (`str`): Relative path to the input csv file.
    """
    try:
        file_name = sys.argv[1]
    except IndexError:
        print("Usage: python3 grade_calculator.py <filename>")
        sys.exit(1)
    if not file_name.endswith(".csv"):
        print("File must be a .csv file")
        sys.exit(1)
    return file_name


def read_csv(file_name):
    """
    Reads the csv file and returns the course name, desired average, hand-in weights and hand-in grades.
    WARNING: This function assumes the csv file is correctly formatted and trusts the user to use `eval()` responsibly.

    Args:
        `file_name` (`str`): Relative path to the input csv file.

    Returns:
        `course_name` (`str`): Name of the course.
        `desired_average` (`float`): Desired average in the course.
        `list` of `HandIn`: List containing course hand-in types with their respective weights and grades.
    """
    # validate file exists
    try:
        with open(file_name, "r") as file:
            data = file.read()
    except FileNotFoundError:
        print(f"File {file_name} not found")
        sys.exit(1)

    lines = [line.split(",") for line in data.split("\n")]

    # read general info about course
    course_name = lines.pop(0)[0]
    desired_average = float(lines.pop(0)[0])

    # read the hand-in category names and weights
    hand_ins = {}
    for line in lines:
        if len(line) == 2:
            name, weight = line
            hand_ins[name] = HandIn(name, eval(weight))
        if len(line) == 3:
            name, grade = line[0:2]
            hand_ins[name].grades.append(eval(grade))

    return course_name, desired_average, hand_ins


if __name__ == "__main__":
    main()
