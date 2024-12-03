def read_data(filename):
    """reads in data about treasures.
    Each treasure has a name, value, and weight

    filename: string. Name of a CSV file where treasures
        are listed 1 per line.
    return: a list of records (dictionaries). Each record
        has the keys "name", "value", and "weight"
    """
    f = open(filename, "r")
    L = []
    for line in f:
        line = line.rstrip().split(",")
        treasure = {"name": line[0], "value": int(line[1][1:]), "weight": int(line[2])}
        L.append(treasure)
    return L


# file = "room1.txt"
# treasures = read_data(file)
# print(treasures)
