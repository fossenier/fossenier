with open("output.csv", "w") as o:
    lines = []
    with open("input.csv", "r") as f:
        for line in f:
            new_line = "["
            for tile in line.rstrip().split(","):
                new_line += f'"{tile.lower()}",'
            lines.append(new_line[:-1] + "],\n")
    o.writelines(lines)