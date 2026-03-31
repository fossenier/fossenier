import csv

mapping = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Somewhat Disagree": 3,
    "Neither Agree nor Disagree": 4,
    "Somewhat Agree": 5,
    "Agree": 6,
    "Strongly Agree": 7
}

# Canonical question ordering
questions = [
"I think it is easy to learn how to play the game.",
"I find the controls of the game to be straightforward.",
"I always know how to achieve my goals/objectives in the game.",
"I find the game’s interface to be easy to navigate.",
"I do not need to go through a lengthy tutorial or read a manual to play the game.",
"I find the game’s menus to be user friendly.",
"I feel the game trains me well in all of the controls.",
"I always know my next goal when I finish an event in the game.",
"I feel the game provides me the necessary information to accomplish a goal within the game.",
"I think the information provided in the game (e.g., onscreen messages, help) is clear.",
"I feel very confident while playing the game.",
"I think the game is fun.",
"I enjoy playing the game.",
"I feel bored while playing the game.",
"I am likely to recommend this game to others.",
"If given the chance, I want to play this game again.",
"I enjoy the sound effects in the game.",
"I enjoy the music in the game.",
"I feel the game’s audio (e.g., sound effects, music) enhances my gaming experience.",
"I think the game’s audio fits the mood or style of the game.",
"I enjoy the game’s graphics.",
"I think the graphics of the game fit the mood or style of the game.",
"I think the game is visually appealing."
]

categories = [
    (1, 11),
    (12, 16),
    (17, 20),
    (21, 23)
]

filename = "406results.csv"

with open(filename, newline='', encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    # Build lookup: question_number -> column index in CSV
    col_lookup = {}

    for i, q in enumerate(questions, start=1):
        if q in header:
            col_lookup[i] = header.index(q)

    sums = {i:0 for i in range(1,24)}
    counts = {i:0 for i in range(1,24)}

    for row in reader:
        for qnum, col in col_lookup.items():
            if col >= len(row):
                continue

            val = row[col].strip()

            if val in mapping:
                sums[qnum] += mapping[val]
                counts[qnum] += 1

column_avgs = {}

for i in range(1,24):
    if counts[i] > 0:
        column_avgs[i] = sums[i] / counts[i]
    else:
        column_avgs[i] = None

category_avgs = []

for start, end in categories:
    total = 0
    count = 0

    for i in range(start, end+1):
        if column_avgs[i] is not None:
            total += column_avgs[i]
            count += 1

    category_avgs.append(total / count if count else None)

print("Column averages:")
for i in range(1,24):
    print(i, column_avgs[i])

print("\nCategory averages:")
for i, avg in enumerate(category_avgs, 1):
    print(f"Category {i}: {avg}")