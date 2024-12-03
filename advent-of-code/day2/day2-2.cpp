#include <fstream>
#include <iostream>
#include <sstream>

bool dampen(std::vector<int> intList, int index);
bool safetyCheck(std::vector<int> intList, bool wasDampened);

int main()
{
    // Open the input file
    std::ifstream infile("day2.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    int safeCount{0};

    std::string line{};
    while (std::getline(infile, line))
    {
        // Split the report into a vector of integers
        std::vector<int> intList{};
        std::istringstream iss(line);
        int num;
        while (iss >> num)
        {
            intList.push_back(num);
        }

        // Check the safety of the report
        if (safetyCheck(intList, false))
        {
            safeCount++;
            // std::cout << "Safe!\n";
        }
        else
        {
            // std::cout << "Unsafe!\n";
        }
    }
    infile.close();
    std::cout << "Safe count: " << safeCount << '\n';
}

bool safetyCheck(std::vector<int> intList, bool wasDampened)
{
    int prevChange{0};
    for (int i{0}; i < intList.size(); ++i)
    {
        if (i == 0)
        {
            continue;
        }

        // std::cout << "Comparing [i]: " << intList[i] << " With [i - 1]: " << intList[i - 1] << '\n';

        int change{intList[i] - intList[i - 1]};

        bool decreasing = change < 0 && prevChange <= 0;
        bool increasing = change > 0 && prevChange >= 0;

        // Unsafe!!!
        if (!(decreasing || increasing))
        {
            // Try and recover
            if (!wasDampened)
            {
                return dampen(intList, i);
            }
            else
            {
                return false;
            }
        }

        // Unsafe!!!
        if (abs(change) > 3 || abs(change) == 0)
        {
            if (!wasDampened)
            {
                return dampen(intList, i);
            }
            else
            {
                return false;
            }
        }
        prevChange = change;
    }
    return true;
}

bool dampen(std::vector<int> intList, int index)
{
    for (int j{-2}; j <= 2; ++j)
    {
        int target = index + j;
        if (target >= 0 && target < intList.size())
        {
            int val = intList[target];
            intList.erase(intList.begin() + target);
            if (safetyCheck(intList, true))
            {
                return true;
            }
            intList.insert(intList.begin() + target, val);
        }
    }
    return false;
}