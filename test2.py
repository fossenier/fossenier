alphabet = "abcdefghijklmnopqrstuvwxyz"
storage = {c: i for i, c in enumerate(alphabet)}  # Create example dictionary

with open("output.txt", "w") as f:
    for key, value in storage.items():
        f.write("a" + "\n")
        f.write(key + "\n")
        f.write(f"{value}" + "\n")
