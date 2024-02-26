# 3
# 11 3 3

# get the populations
# determine differences
# pick the n biggest

region_count = int(input(""))
regions = [int(region) for region in input("").split(" ")]

# determine the number of regions that can be won without winning
max_lose = int(region_count / 2)

# pick those biggest regions
regions.sort(reverse=True)
biggest_regions = regions[:max_lose]
smallest_regions = regions[max_lose:]

max_votes = 0
for region in biggest_regions:
    max_votes += region
for region in smallest_regions:
    max_votes += int(region / 2)

print(max_votes)
