#include <fstream>
#include <iostream>
#include <set>
#include <vector>

int tallyTrailheads(std::vector<std::vector<int>> &topography);
std::set<std::pair<int, int>> scoreTrailheads(std::vector<std::vector<int>> &topography, int x, int y, std::vector<std::vector<bool>> &visited);

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
        for (char c : line)
        {
            if (isdigit(c))
            {
                row.push_back(c - '0');
            }
        }
        topography.push_back(row);
    }

    // Print the topography for debugging
    for (const auto &row : topography)
    {
        for (int height : row)
        {
            std::cout << height << ' ';
        }
        std::cout << '\n';
    }

    int result = tallyTrailheads(topography);
    std::cout << "Result: " << result << '\n';
}

/**
 * Recursive function to calculate reachable summits from a given position.
 * Only valid moves are up, down, left, or right.
 */
std::set<std::pair<int, int>> scoreTrailheads(std::vector<std::vector<int>> &topography, int x, int y, std::vector<std::vector<bool>> &visited)
{
    if (visited[y][x])
    {
        return {};
    }
    visited[y][x] = true;

    std::set<std::pair<int, int>> summits;

    // If this position is a summit, add it and return.
    if (topography[y][x] == 9)
    {
        summits.insert({x, y});
        return summits;
    }

    // Valid moves: up, down, left, right
    const int dx[] = {0, 0, -1, 1};
    const int dy[] = {-1, 1, 0, 0};

    for (int direction = 0; direction < 4; ++direction)
    {
        int nx = x + dx[direction];
        int ny = y + dy[direction];

        // Check boundaries and height difference
        if (nx >= 0 && nx < topography[0].size() && ny >= 0 && ny < topography.size() &&
            topography[ny][nx] == topography[y][x] + 1)
        {
            auto reachableSummits = scoreTrailheads(topography, nx, ny, visited);
            summits.insert(reachableSummits.begin(), reachableSummits.end());
        }
    }

    return summits;
}

/**
 * Tally the total score for all trailheads (positions with height 0).
 */
int tallyTrailheads(std::vector<std::vector<int>> &topography)
{
    int sum = 0;

    for (int y = 0; y < topography.size(); ++y)
    {
        for (int x = 0; x < topography[0].size(); ++x)
        {
            if (topography[y][x] == 0) // Trailhead
            {
                std::vector<std::vector<bool>> visited(topography.size(), std::vector<bool>(topography[0].size(), false));
                std::set<std::pair<int, int>> summits = scoreTrailheads(topography, x, y, visited);

                std::cout << "Trailhead: (" << y << ", " << x << ") -> " << summits.size() << " summits\n";

                sum += summits.size();
            }
        }
    }

    return sum;
}