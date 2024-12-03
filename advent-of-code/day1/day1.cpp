#include <fstream>
#include <iostream>

int main()
{
    std::ifstream infile("day1.txt");

    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    long long int sum = 0;

    // Create a list to hold many integers
    std::vector<int> lIntList;
    std::vector<int> rIntList;

    std::string strInput{};
    while (std::getline(infile, strInput))
    {
        // Split the string into two parts splitting on the "   "
        std::string strPart1 = strInput.substr(0, strInput.find("   "));
        std::string strPart2 = strInput.substr(strInput.find("   ") + 3);

        // Convert the strings to integers
        int intPart1 = std::stoi(strPart1);
        int intPart2 = std::stoi(strPart2);

        // Add the integers to the end of the list
        lIntList.push_back(intPart1);
        rIntList.push_back(intPart2);
    }
    infile.close();

    // Sort the lists in ascending order
    std::sort(lIntList.begin(), lIntList.end());
    std::sort(rIntList.begin(), rIntList.end());

    // Iterate through the indices of both lists and access the values
    for (int i{0}; i < lIntList.size(); ++i)
    {
        sum += abs(lIntList[i] - rIntList[i]);
    }

    std::cout << "Sum: " << sum << '\n';

    return 0;
}