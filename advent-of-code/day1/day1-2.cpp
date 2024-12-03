#include <fstream>
#include <iostream>
#include <map>

int main()
{
    std::ifstream infile("day1.txt");

    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    long long int sum{0};

    // Hold the left values and count the right hand values
    std::vector<int> lIntList;
    std::map<int, int> rIntCount;

    std::string strInput{};
    while (std::getline(infile, strInput))
    {
        // Split the string into two parts splitting on the "   "
        std::string lStr{strInput.substr(0, strInput.find("   "))};
        std::string rStr{strInput.substr(strInput.find("   ") + 3)};

        // Convert the strings to integers
        int lInt{std::stoi(lStr)};
        int rInt{std::stoi(rStr)};

        // Add the left integer to the list
        lIntList.push_back(lInt);

        // Count the right integer
        rIntCount[rInt]++;
    }
    infile.close();

    // Iterate through the indices of both lists and access the values
    for (int i{0}; i < lIntList.size(); ++i)
    {
        sum += (lIntList[i] * rIntCount[lIntList[i]]);
    }

    std::cout << "Sum: " << sum << '\n';

    return 0;
}