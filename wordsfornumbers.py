BASE = [
    "unused",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
TEN_TO_TWENTY = [
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]
TEN_TO_HUNDRED = [
    "",
    "ten",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]


def main():
    try:
        while True:
            text_tokens = input("").split(" ")
            for i, text_token in enumerate(text_tokens):
                if text_token.isnumeric():
                    number_as_word = number_to_word(int(text_token))
                    if i == 0:
                        number_as_word = number_as_word.capitalize()
                    text_tokens[i] = number_as_word
            print(" ".join(text_tokens))
    except EOFError:
        pass


def number_to_word(number):
    if 1 <= number <= 9:
        return BASE[number]
    elif 10 <= number <= 19:
        return TEN_TO_TWENTY[number - 10]
    elif 20 <= number <= 99:
        new_number = TEN_TO_HUNDRED[number // 10]
        if number % 10 != 0:
            new_number += "-" + BASE[number % 10]
        return new_number
    else:
        return str(number)


if __name__ == "__main__":
    main()
