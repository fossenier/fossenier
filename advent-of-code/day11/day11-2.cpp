#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

void blink(std::vector<long int> &stones);

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

    for (int i = 0; i < 75; i++)
    {
        blink(stones); // Modify the vector in place
    }

    std::cout << "Size: " << stones.size() << '\n';

    return 0;
}

void blink(std::vector<long int> &stones)
{
    std::vector<long int> result;
    result.reserve(stones.size() * 2); // Reserve enough memory to avoid reallocations

    for (long int stone : stones)
    {
        if (stone == 0)
        {
            result.push_back(1);
            continue;
        }

        int digits = 0;
        for (long int temp = stone; temp > 0; temp /= 10)
        {
            digits++;
        }

        if (digits % 2 == 0)
        {
            std::string stone_str = std::to_string(stone);
            std::string first_half = stone_str.substr(0, stone_str.size() / 2);
            std::string second_half = stone_str.substr(stone_str.size() / 2);

            result.push_back(std::stol(first_half));
            result.push_back(std::stol(second_half));
        }
        else
        {
            result.push_back(stone * 2024);
        }
    }

    // Directly swap to avoid unnecessary copying
    stones.swap(result);
}