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
    if (array[row][col] != 'A')
    {
        return 0;
    }

    // 1 . 2
    // . A .
    // 3 . 4

    bool onefour{false};
    bool fourone{false};

    bool twothree{false};
    bool threetwo{false};

    if (row - 1 >= 0 && col - 1 >= 0 && row + 1 < array.size() && col + 1 < array[row].size())
    {
        onefour = array[row - 1][col - 1] == 'M' && array[row + 1][col + 1] == 'S';
    }

    if (row - 1 >= 0 && col + 1 < array[row].size() && row + 1 < array.size() && col - 1 >= 0)
    {
        fourone = array[row - 1][col - 1] == 'S' && array[row + 1][col + 1] == 'M';
    }

    if (row - 1 >= 0 && col + 1 < array[row].size() && row + 1 < array.size() && col - 1 >= 0)
    {
        twothree = array[row - 1][col + 1] == 'M' && array[row + 1][col - 1] == 'S';
    }

    if (row - 1 >= 0 && col + 1 < array[row].size() && row + 1 < array.size() && col - 1 >= 0)
    {
        threetwo = array[row - 1][col + 1] == 'S' && array[row + 1][col - 1] == 'M';
    }

    if ((onefour || fourone) && (twothree || threetwo))
    {
        return 1;
    }
    else
    {
        return 0;
    }
}