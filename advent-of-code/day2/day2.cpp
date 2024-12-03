#include <fstream>
#include <iostream>
#include <sstream>

int main()
{
    std::ifstream in("day2.txt");

    if (!in)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    long long int safeCount{0};

    std::string strInput{};
    while (std::getline(in, strInput))
    {
        // Split the string into a vector of integers on the " "
        std::vector<int> intList{};
        // Attempt to extract integers from the string
        std::istringstream iss(strInput);
        int num;
        while (iss >> num)
        {
            intList.push_back(num);
        }

        // Iterate through the list of integers
        int lastStep{0};
        bool unsafe{false};
        for (int i{0}; i < intList.size(); ++i)
        {
            // There is no change in the first element
            if (i == 0)
            {
                continue;
            }

            // Make sure the change is 1, 2, or 3
            int step{intList[i] - intList[i - 1]};
            if (abs(step) > 3 || abs(step) == 0)
            {
                unsafe = true;
                break;
            }
            // Decreasing
            if (lastStep <= 0 && step < 0)
            {
                lastStep = step;
                continue;
            }
            // Increasing
            else if (lastStep >= 0 && step > 0)
            {
                lastStep = step;
                continue;
            }
            // Changed between increasing and decreasing
            unsafe = true;
            break;
        }

        if (!unsafe)
        {
            safeCount++;
        }
    }
    in.close();

    std::cout << "Safe count: " << safeCount << '\n';
}