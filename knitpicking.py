def main():
    # The number of sock types to be stored
    n = int(input("").rstrip())

    # A dict containing all sock varieties, and their respective feet quantities
    # (left, right, any)
    sock_drawer = {}

    # Collect socks from user input
    for _ in range(n):
        variety, foot, quantity = input("").rstrip().split(" ")
        quantity = int(quantity)

        if variety not in sock_drawer:
            sock_drawer[variety] = {"left": 0, "right": 0, "any": 0}

        # Track how many left, right, and any socks there are for each variety
        sock_drawer[variety][foot] += quantity

    # Determine the number of drawings
    drawings = unluckiest_drawing(sock_drawer)

    if drawings == -1:
        print("impossible")
    else:
        print(drawings)


def unluckiest_drawing(socks) -> int:
    """
    Determines the most socks you need to grab before you get a match of the
    same variety, and which could be worn on both feet.
    -1 if no match is possible
    """

    def maximize_draws(sock) -> int:
        """
        Maximizes the number of sock draws for one type with no match.
        """
        left = sock["left"]
        right = sock["right"]
        any = sock["any"]

        # Grab as many right / left socks as possible, whichever has more
        if left > 0:
            if right > left:
                return right
            else:
                return left
        # But only grab from one type, otherwise you would match
        elif right > 0:
            return right
        # If there's no right / left socks, and there's an "any", grab one
        elif any > 0:
            return 1

    def check_match(sock) -> bool:
        """
        Check to see if a variety can have a match.
        """
        left = sock["left"] > 0
        right = sock["right"] > 0
        any = sock["any"] > 0

        if left and right:
            return True
        elif any and (left or right):
            return True
        elif sock["any"] >= 2:
            return True

    drawing_tally = 0
    can_match = False
    for variety in socks:
        # See if at least one variety matches
        can_match = can_match or check_match(socks[variety])

        # Tally the unluckiest series of socks to draw
        drawing_tally += maximize_draws(socks[variety])

    # The biggest number of socks with no match is obvious, it's all of them
    if not can_match:
        return -1
    # The biggest number of socks with no matches, plus the one sock to match
    else:
        return drawing_tally + 1


if __name__ == "__main__":
    main()
