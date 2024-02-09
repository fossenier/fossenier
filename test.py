# suits = ["H", "D", "S", "C"]
# values = ["A", *[str(v) for v in range(2, 11)], "J", "Q", "K"]
# cards = []
# for s in suits:
#     for v in values:
#         cards.append(s + v)
# print(len(cards))


def recursive_list_sort(unsorted_list):
    """
    Purpose:
        Recursively dive into a list containing one of int / float / str
        and also lists following the same rule, and sort each sublist encountered.
        Post-conditions:
            (none)
        Return:
            The sorted list.
    """
    # copy the list to leave the original untouched
    sorted_list = unsorted_list.copy()
    lists = []
    # mark down each sublist
    for item in sorted_list:
        if type(item) is list:
            lists.append(item)
    # remove each sublist from the sorted list, and then sort it in spot
    for i in range(len(lists)):
        sorted_list.remove(lists[i])
        lists[i] = recursive_list_sort(lists[i])
    # sort the sorted list, now that the sublists are gone
    sorted_list.sort()
    # add back the now sorted lists
    sorted_list.extend(lists)
    return sorted_list


x = [[1, 0], "1", "7", "a", "4.0", ["1", "-2"], ["0", ["3", "2", "a", [0, 1]]]]
print(recursive_list_sort(x))
print(x)
