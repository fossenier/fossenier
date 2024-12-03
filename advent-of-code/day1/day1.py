def main():
    distance = 0
    with open("day1.txt", "r") as f:
        ldata, rdata = list(), list()
        data = [line.split("   ") for line in f.readlines()]
        for datum in data:
            ldata.append(datum[0])
            rdata.append(datum[1])
        ldata.sort()
        rdata.sort()
        for i in range(len(ldata)):
            distance += abs(int(ldata[i]) - int(rdata[i]))
    print(distance)


if __name__ == "__main__":
    main()
