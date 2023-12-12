def palindrome(word):
    if len(word) < 2:
        return True
    return word[0] == word[-1] and palindrome(word[1 : len(word) - 1])


print(palindrome("kayak"))
