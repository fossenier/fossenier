CHARACTER_TO_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "_": "..--",
    ".": "---.",
    ",": ".-.-",
    "?": "----",
}

MORSE_TO_CHARACTER = {value: key for key, value in CHARACTER_TO_MORSE.items()}


def main():
    final_messages = []
    try:
        while True:
            data_in = input("")
            final_message = ""
            intermediary_morse, number_decoding = decode(data_in)
            for number in reversed(number_decoding):
                final_message += MORSE_TO_CHARACTER[intermediary_morse[:number]]
                intermediary_morse = intermediary_morse[number:]
            final_messages.append(final_message)
    except EOFError:
        pass
    for final_message in final_messages:
        print(final_message)


def decode(data_in):
    intermediary_morse = ""
    number_decoding = []
    for c in data_in:
        intermediary_character = CHARACTER_TO_MORSE[c]
        intermediary_morse += intermediary_character
        number_decoding.append(len(intermediary_character))
    return intermediary_morse, number_decoding


if __name__ == "__main__":
    main()
