#include <iostream>
#include <fstream>

std::vector<long int> blink(std::vector<long int> &stones, bool &flag);

int main()
{
    std::ifstream infile("day11.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<long int> stones;

    long int stone;
    while (infile >> stone)
    {
        stones.push_back(stone);
    }

    bool overflowed{false};
    for (int i{0}; i < 25; i++)
    {
        stones = blink(stones, overflowed);
        if (overflowed)
        {
            std::cout << "Overflowed\n";
            break;
        }
    }

    std::cout << "Result: ";
    for (long int stone : stones)
    {
        std::cout << stone << ' ';
    }
    std::cout << '\n';

    std::cout << "Size: " << stones.size() << '\n';
}

std::vector<long int> blink(std::vector<long int> &stones, bool &flag)
{
    std::vector<long int> result;

    for (long int stone : stones)
    {
        if (stone == 0)
        {
            result.push_back(1);
            continue;
        }
        // The number of digits in the stone
        int digits{0};
        for (long int temp{stone}; temp > 0; temp /= 10)
        {
            digits++;
        }
        if (digits % 2 == 0)
        {
            std::string stone_str{std::to_string(stone)};
            // Split the string in half
            std::string first_half{stone_str.substr(0, stone_str.size() / 2)};
            std::string second_half{stone_str.substr(stone_str.size() / 2)};

            result.push_back(std::stol(first_half));
            result.push_back(std::stol(second_half));
            continue;
        }

        long int new_value = stone * 2024;
        if (new_value / 2024 != stone)
        {
            flag = true;
        }
        result.push_back(new_value);
    }

    return result;
}