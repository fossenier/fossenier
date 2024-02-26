data_in = input("")

vowels = ["a", "e", "i", "o", "u"]

vowel_count = 0
y_count = 0

for char in data_in:
    if char in vowels:
        vowel_count += 1
    elif char == "y":
        y_count += 1

print(vowel_count, vowel_count + y_count)
