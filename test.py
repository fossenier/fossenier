import random


def generate_test_input():
    commands = []
    keys = []
    used_values = set()

    # Generate 200 add commands
    for _ in range(200):
        key = f"key_{random.randint(1, 1000)}"
        value = round(random.uniform(1.0, 100.0), 2)
        while value in used_values:
            value = round(random.uniform(1.0, 100.0), 2)
        used_values.add(value)

        option = random.choice(["k", "v", "a"])  # Randomly select the option
        commands.append(f"a {option}\n{key} {value}")
        keys.append(key)

    # Generate remove commands interspersed with add commands
    remove_chance = 0.3  # 30% chance to remove a key
    for _ in range(100):  # Add some more operations
        if keys and random.random() < remove_chance:
            key_to_remove = random.choice(keys)
            commands.append(f"r\n{key_to_remove}")
            keys.remove(key_to_remove)
        else:
            key = f"key_{random.randint(1, 1000)}"
            value = round(random.uniform(1.0, 100.0), 2)
            while value in used_values:
                value = round(random.uniform(1.0, 100.0), 2)
            used_values.add(value)

            option = random.choice(["k", "v", "a"])
            commands.append(f"a {option}\n{key} {value}")
            keys.append(key)

    # Taper down by removing all remaining keys
    while keys:
        key_to_remove = keys.pop()
        commands.append(f"r\n{key_to_remove}")

    # Write to a file
    with open("test_input.txt", "w") as file:
        file.write("\n".join(commands))

    print("Test input written to test_input.txt")


if __name__ == "__main__":
    generate_test_input()
