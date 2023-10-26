def main():
    letters = {}
    user_word = input("Input a word: ")

    for letter in user_word:
        letters[letter] = 1 + letters.get(letter, 0)

    # visually check that the dictionary is working
    print("Count of each character:")
    for letter in letters:
        print("{}: {}".format(letter, letters.get(letter, "error in my code")))

    result = word_factorial(letters)
    print(
        "The number of possible unique words that can be formed from {} is : {:.0f}".format(
            user_word, result
        )
    )
    return


def word_factorial(dictionary):
    word_length = 0
    denominator = 1
    for letter in dictionary:
        letter_count = dictionary.get(letter, 0)
        word_length += letter_count
        denominator *= factorial(letter_count)
    print("Word length", word_length)
    numerator = factorial(word_length)
    result = numerator / denominator
    return result


def factorial(number):
    if number == 1:
        return 1
    else:
        return number * factorial(number - 1)


if __name__ == "__main__":
    main()
