x = [1, 2, 3, 3]

new_list = []

# for value in x:
#     if value not in new_list:
#         new_list.append(value)

while len(x) != 0:
    value = x.pop()
    if value not in new_list:
        new_list.append(value)
for i in range(len(new_list) - 1, -1, -1):
    x.append(new_list[i])

print(x, new_list)
