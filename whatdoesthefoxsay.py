# 1
# toot woof wa ow ow ow pa blub blub pa toot pa blub pa pa ow pow toot
# dog goes woof
# fish goes blub
# elephant goes toot
# seal goes ow
# what does the fox say?

test_case_count = int(input(""))
for _ in range(test_case_count):
    unknown_sounds = input("").split(" ")
    known_sounds = []
    info = input("")
    while info != "what does the fox say?":
        known_sounds.append(info.split(" ")[-1])
        info = input("")
    fox_sounds = ""
    for sound in unknown_sounds:
        if sound not in known_sounds:
            fox_sounds += sound + " "
    print(fox_sounds.rstrip())


# expected
# wa pa pa pa pa pa pow
