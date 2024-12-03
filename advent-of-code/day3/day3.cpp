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

    std::regex pattern(R"(mul\(([0-9]{1,3}),([0-9]{1,3})\))");

    auto matches_begin = std::sregex_iterator(input.begin(), input.end(), pattern);
    auto matches_end = std::sregex_iterator();

    long long int total{0};

    for (std::sregex_iterator it = matches_begin; it != matches_end; ++it)
    {
        std::smatch match = *it;

        int m1 = std::stoi(match[1].str());
        int m2 = std::stoi(match[2].str());

        total += (m1 * m2);
    }

    std::cout << "Summation: " << total << '\n';

    return 0;
}