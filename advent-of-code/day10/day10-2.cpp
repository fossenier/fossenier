#include <fstream>
#include <iostream>
#include <set>
#include <vector>

int tallyTrailheadRatings(std::vector<std::vector<int>> &topography);
int rateTrailheads(std::vector<std::vector<int>> &topography, int x, int y, int currentHeight);

int main()
{
    std::ifstream infile("day10.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<std::vector<int>> topography;

    std::string line;
    while (std::getline(infile, line))
    {
        std::vector<int> row;
        // Read in a line of digits 0-9 and add them to the row
        for (char c : line)
        {
            if (isdigit(c))
            {
                row.push_back(c - '0');
            }
        }
        topography.push_back(row);
    }

    // Print the topography
    for (const auto &row : topography)
    {
        for (int val : row)
        {
            std::cout << val << ' ';
        }
        std::cout << '\n';
    }

    int result = tallyTrailheadRatings(topography);
    std::cout << "Result: " << result << '\n';
}

int tallyTrailheadRatings(std::vector<std::vector<int>> &topography)
{
    int totalRating = 0;

    for (int y = 0; y < topography.size(); ++y)
    {
        for (int x = 0; x < topography[0].size(); ++x)
        {
            if (topography[y][x] == 0) // Check if the position is a trailhead
            {
                std::vector<std::vector<bool>> visited(topography.size(), std::vector<bool>(topography[0].size(), false));
                int rating = rateTrailheads(topography, x, y, 0);
                totalRating += rating;

                std::cout << "Trailhead at (" << y << ", " << x << ") has a rating of " << rating << '\n';
            }
        }
    }

    return totalRating;
}

int rateTrailheads(std::vector<std::vector<int>> &topography, int x, int y, int currentHeight)
{
    if (x < 0 || x >= topography[0].size() || y < 0 || y >= topography.size())
        return 0; // Out of bounds
    if (topography[y][x] != currentHeight)
        return 0; // Not the correct height for continuation of the trail

    // If current position is a summit (height 9), this is one valid path
    if (topography[y][x] == 9)
        return 1;

    // Explore all possible moves (up, down, left, right)
    int rating = 0;
    rating += rateTrailheads(topography, x + 1, y, currentHeight + 1); // Right
    rating += rateTrailheads(topography, x - 1, y, currentHeight + 1); // Left
    rating += rateTrailheads(topography, x, y + 1, currentHeight + 1); // Down
    rating += rateTrailheads(topography, x, y - 1, currentHeight + 1); // Up

    return rating; // Return total number of paths
}