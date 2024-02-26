friend_count, friendship_pairs_count = [int(number) for number in input("").split(" ")]

# initialize friends' success vs. friendships
friend_success = {}
for success_factor in range(1, friend_count + 1):
    friend_success[success_factor] = 0

for _ in range(friendship_pairs_count):
    friendship_pair = input("").split(" ")
    for i in range(2):
        friend_success[int(friendship_pair[i])] += 1


result = ""
for friend in friend_success:
    marketability_coefficient = friend_success[friend] - friend
    result += str(marketability_coefficient) + " "

print(result[:-1])
