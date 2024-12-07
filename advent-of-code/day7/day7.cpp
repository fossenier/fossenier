#include <fstream>
#include <iostream>
#include <sstream>

long long countSolves(std::vector<long long> unsolved, long long result);

int main()
{
    std::ifstream infile("day7.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    long long total{0};

    std::string line{};
    while (std::getline(infile, line))
    {
        std::vector<long long> unsolved;

        std::istringstream iss(line);
        std::string num;
        // Read in the numbers
        // ex line)
        // 190: 10 19
        // ex vector
        // 190, 10, 19
        while (std::getline(iss, num, ' '))
        {
            // to long long int
            unsolved.push_back(std::stol(num));
        }

        long long result = countSolves(std::vector<long long>(unsolved.begin() + 1, unsolved.end()), unsolved[0]);
        // std::cout << "Result: " << result << '\n';
        // for (auto i : unsolved)
        // {
        //     std::cout << i << ' ';
        // }
        // std::cout << '\n';
        if (result > 0)
        {
            total += unsolved[0];
        }
    }

    std::cout << "Total: " << total << '\n';
}

// ERROR, this is not solving properly
long long countSolves(std::vector<long long> unsolved, long long result)
{
    if (unsolved.size() == 1)
    {
        if (unsolved[0] == result)
        {
            return 1;
        }
        else
        {
            return 0;
        }
    }

    // Given [7, 12, 3] and result = 57
    // The answer is 7 + 12 * 3 = 57
    // So, simulate this, first by trying 57 / 3 = 19
    // Then, try 57 - 3 = 54
    long long count{0};

    count += countSolves(std::vector<long long>(unsolved.begin(), unsolved.end() - 1), result - unsolved[unsolved.size() - 1]);
    if (result % unsolved[unsolved.size() - 1] == 0)
    {
        count += countSolves(std::vector<long long>(unsolved.begin(), unsolved.end() - 1), result / unsolved[unsolved.size() - 1]);
    }

    return count;
}

// // if result = 57 and num = 7, return 5 (becase 5 (+++) 7 = 57)
// // if result = 2972 and num = 72, return 29 (becase 29 (+++) 72 = 2972)
// // This is essentially treating the number as strings for concatenation, deconcatenate
// long long unglue(long long result, long long num)
// {
//     std::string resultStr = std::to_string(result);
//     std::string numStr = std::to_string(num);

//     if (resultStr.size() <= numStr.size() || resultStr.substr(resultStr.size() - numStr.size()) != numStr)
//     {
//         return -1; // Invalid case
//     }

//     std::string prefix = resultStr.substr(0, resultStr.size() - numStr.size());
//     return std::stoll(prefix);
// }