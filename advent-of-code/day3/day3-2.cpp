#include <iostream>
#include <fstream>
#include <string>
#include <regex>

int main()
{
    std::ifstream infile("day3.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::string input((std::istreambuf_iterator<char>(infile)),
                      std::istreambuf_iterator<char>());

    std::regex pattern1(R"(mul\(([0-9]{1,3}),([0-9]{1,3})\))");
    std::regex pattern2(R"(do\(\))");
    std::regex pattern3(R"(don't\(\))");

    bool enabled = true;

    std::regex combinedPattern(R"((mul\(([0-9]{1,3}),([0-9]{1,3})\))|(do\(\))|(don't\(\)))");
    auto matches_begin = std::sregex_iterator(input.begin(), input.end(), combinedPattern);
    auto matches_end = std::sregex_iterator();

    long long int total{0};

    for (std::sregex_iterator it = matches_begin; it != matches_end; ++it)
    {
        std::smatch match = *it;

        if (match[1].matched)
        {
            if (enabled)
            {
                int m1 = std::stoi(match[2].str());
                int m2 = std::stoi(match[3].str());

                total += (m1 * m2);
            }
        }
        // do()
        else if (match[4].matched)
        {
            enabled = true;
        }
        // don't()
        else if (match[5].matched)
        {
            enabled = false;
        }
    }

    std::cout << "Summation: " << total << '\n';

    return 0;
}