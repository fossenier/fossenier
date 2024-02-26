from math import sqrt

plot_count, circle_house_count, square_house_count = [
    int(number) for number in input("").split(" ")
]

plot_radius_list = [int(number) for number in input("").split(" ")]
house_radius_list = [int(number) for number in input("").split(" ")]
house_length_list = [int(number) for number in input("").split(" ")]

# turn the squre houses into circle houses (diagonal = 2 * radius)
for square_house in house_length_list:
    house_diagonal = sqrt(square_house**2 * 2)
    house_radius_list.append(house_diagonal / 2)

house_radius_list.sort(reverse=True)
plot_radius_list.sort(reverse=True)

max_plot_fill = 0

while house_radius_list and plot_radius_list:
    print(house_radius_list, plot_radius_list)
    if house_radius_list[0] < plot_radius_list[0]:
        max_plot_fill += 1
        plot_radius_list.pop(0)
    house_radius_list.pop(0)

print(max_plot_fill)
