"""
A program to calculate my average in the class.
"""

import csv as csv

DESIRED_GRADE = 80
FILENAME = "phys115marks.csv"
TYPES = ["assignments", "midterm", "final", "labreports", "labtests"]
WEIGHTS = {
    "assignments": 10,
    "midterm": 25,
    "final": 50,
    "labreports": 15 * (2 / 3),
    "labtests": 15 * (1 / 3),
}


def main():
    grade_data = read_grade_data(FILENAME)
    averages = calculate_averages(grade_data, TYPES)
    zero_corrected_average, weighted_average = calculate_class_average(
        averages, TYPES, WEIGHTS
    )
    print_averages(
        zero_corrected_average,
        weighted_average,
        averages,
        TYPES,
        WEIGHTS,
        DESIRED_GRADE,
    )


def calculate_averages(grade_data, types):
    averages = {}
    for type in types:
        averages[type] = []
    for data in grade_data:
        averages[data[0]].append(data[1])
    for average in averages:
        grade_sum, grade_count = 0, 0
        for grade in averages[average]:
            grade_sum += grade
            grade_count += 1
        averages[average] = 0 if grade_count == 0 else grade_sum / grade_count
    return averages


def calculate_class_average(averages, types, weights):
    class_weighted_average, non_zero_weight_sum = 0, 0
    for type in types:
        average = averages[type]
        weight = weights[type]
        class_weighted_average += average * weight
        print(f"average: {average}, weight: {weight}")
        if average != 0:
            non_zero_weight_sum += weight

    # determine modifier for just non-zero grades
    non_zero_weight_modifier = 100 / non_zero_weight_sum

    # convert to percent after multiplying by weights
    return (
        class_weighted_average * non_zero_weight_modifier / 100,
        class_weighted_average / 100,
    )


def print_averages(average, weighted_average, averages, types, weights, desired_grade):
    print("\nOverall PHYS-115 Grade to Date")
    print(f"{average}\n")

    for type in types:
        print(f"{type.capitalize()}: {averages[type]}")

    print("\nCurrent Weighted Average")
    print(f"{weighted_average}\n")

    print(f"Final Grade Needed For {desired_grade}%")
    print("{:.2f}%".format((desired_grade - weighted_average) * 100 / weights["final"]))


def read_grade_data(filename):
    grade_data = []
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            grade_data.append((row[0], float(row[1])))
    return grade_data


if __name__ == "__main__":
    main()
