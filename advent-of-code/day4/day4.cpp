#include <fstream>
#include <iostream>

int count_xmas(std::vector<std::vector<char>> array, int row, int col);

int main()
{
    std::ifstream infile("day4.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<std::vector<char>> array;

    std::string line{};
    while (std::getline(infile, line))
    {
        std::vector<char> row;
        for (char c : line)
        {
            row.push_back(c);
        }
        array.push_back(row);
    }
    infile.close();

    // Iterate over every row and column
    int count{0};
    for (int row{0}; row < array.size(); ++row)
    {
        for (int col{0}; col < array[row].size(); ++col)
        {
            count += count_xmas(array, row, col);
        }
    }

    std::cout << "Count: " << count << '\n';
}

int count_xmas(std::vector<std::vector<char>> array, int row, int col)
{
    int count{0};
    if (array[row][col] != 'X')
    {
        return count;
    }

    // Check right (AKA if col + 1 == 'M', col + 2 == 'A', col + 3 == 'S')
    if (col + 3 < array[row].size())
    {
        if (array[row][col + 1] == 'M' && array[row][col + 2] == 'A' && array[row][col + 3] == 'S')
        {
            count++;
        }
    }

    // Check down (AKA if row + 1 == 'M', row + 2 == 'A', row + 3 == 'S')
    if (row + 3 < array.size())
    {
        if (array[row + 1][col] == 'M' && array[row + 2][col] == 'A' && array[row + 3][col] == 'S')
        {
            count++;
        }
    }

    // Check left (AKA if col - 1 == 'M', col - 2 == 'A', col - 3 == 'S')
    if (col - 3 >= 0)
    {
        if (array[row][col - 1] == 'M' && array[row][col - 2] == 'A' && array[row][col - 3] == 'S')
        {
            count++;
        }
    }

    // Check up (AKA if row - 1 == 'M', row - 2 == 'A', row - 3 == 'S')
    if (row - 3 >= 0)
    {
        if (array[row - 1][col] == 'M' && array[row - 2][col] == 'A' && array[row - 3][col] == 'S')
        {
            count++;
        }
    }

    // Check diagonal right down (AKA if row + 1 == 'M', row + 2 == 'A', row + 3 == 'S' and col + 1 == 'M', col + 2 == 'A', col + 3 == 'S')
    if (row + 3 < array.size() && col + 3 < array[row].size())
    {
        if (array[row + 1][col + 1] == 'M' && array[row + 2][col + 2] == 'A' && array[row + 3][col + 3] == 'S')
        {
            count++;
        }
    }

    // Check diagonal left down (AKA if row + 1 == 'M', row + 2 == 'A', row + 3 == 'S' and col - 1 == 'M', col - 2 == 'A', col - 3 == 'S')
    if (row + 3 < array.size() && col - 3 >= 0)
    {
        if (array[row + 1][col - 1] == 'M' && array[row + 2][col - 2] == 'A' && array[row + 3][col - 3] == 'S')
        {
            count++;
        }
    }

    // Check diagonal right up (AKA if row - 1 == 'M', row - 2 == 'A', row - 3 == 'S' and col + 1 == 'M', col + 2 == 'A', col + 3 == 'S')
    if (row - 3 >= 0 && col + 3 < array[row].size())
    {
        if (array[row - 1][col + 1] == 'M' && array[row - 2][col + 2] == 'A' && array[row - 3][col + 3] == 'S')
        {
            count++;
        }
    }

    // Check diagonal left up (AKA if row - 1 == 'M', row - 2 == 'A', row - 3 == 'S' and col - 1 == 'M', col - 2 == 'A', col - 3 == 'S')
    if (row - 3 >= 0 && col - 3 >= 0)
    {
        if (array[row - 1][col - 1] == 'M' && array[row - 2][col - 2] == 'A' && array[row - 3][col - 3] == 'S')
        {
            count++;
        }
    }

    return count;
}