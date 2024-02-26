data_in = input("")
all_data = []
while data_in != "0":
    all_data.append(data_in)
    data_in = input("")
all_data.append("0")

test_cases = []
latest_test_case = []
for data in all_data:
    if data.isnumeric():
        if latest_test_case != []:
            test_cases.append(latest_test_case)
            latest_test_case = []
    else:
        latest_test_case.append(data)
test_cases.append(latest_test_case)


for i, test_case in enumerate(test_cases):
    animals = {}
    for animal in test_case:
        animal_type = animal.split(" ")[-1].lower()
        try:
            animals[animal_type] += 1
        except KeyError:
            animals[animal_type] = 1
    if len(animals) == 0:
        continue
    print(f"List {i + 1}:")
    alphabetical_animals = []
    for animal in animals:
        alphabetical_animals.append(f"{animal} | {animals[animal]}")
    alphabetical_animals.sort()
    for animal_summary in alphabetical_animals:
        print(animal_summary)
