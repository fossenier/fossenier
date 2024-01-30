def copy3(data):
    """
    Copies the given list of data.
    Preconditions:
        :param data: a list
        :param copy: a list with the same contents as data
    Postconditions:
        data becomes empty
    :return: A copy of the list
    """
    copied = []
    for i in range(len(data)):
        d = data[i]
        data.remove(d)
        copied.append(d)
    return copied


x = [1, 2, 3]

y = copy3(x)

print(x, y)
