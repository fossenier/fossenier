#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <vector>

struct point
{
    int x;
    int y;

    bool operator<(const point &other) const
    {
        return std::tie(x, y) < std::tie(other.x, other.y);
    }

    bool operator==(const point &other) const
    {
        return x == other.x && y == other.y;
    }
};

std::set<point> getAntiNodes(std::map<char, std::set<point>> &antenna_locations, int width, int height);

int main()
{
    std::ifstream infile("day8.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::map<char, std::set<point>> antenna_locations;

    std::string file_line{};
    int row{0};
    int col{0};
    while (std::getline(infile, file_line))
    {
        col = 0;
        for (char c : file_line)
        {
            if (c != '.')
            {
                antenna_locations[c].insert(point{row, col});
            }
            col++;
        }
        row++;
    }

    // Example of how to access the map
    for (const auto &pair : antenna_locations)
    {
        std::cout << "Character: " << pair.first << "\nPoints:\n";
        for (const auto &pt : pair.second)
        {
            std::cout << "  (" << pt.x << ", " << pt.y << ")\n";
        }
    }

    std::set<point> anti_nodes = getAntiNodes(antenna_locations, row, col);
    // Count the number of anti-nodes
    std::cout << "Number of anti-nodes: " << anti_nodes.size() << '\n';

    // Display all anti-nodes
    for (const auto &pt : anti_nodes)
    {
        std::cout << "  (" << pt.x << ", " << pt.y << ")\n";
    }

    return 0;
}

std::set<point> getAntiNodes(std::map<char, std::set<point>> &antenna_locations, int width, int height)
{
    std::set<point> anti_nodes;
    for (const auto &[antenna, locations] : antenna_locations)
    {
        for (const auto &location : locations)
        {
            for (const auto &location2 : locations)
            {
                if (location == location2)
                {
                    continue;
                }
                std::cout << "Antenna: " << antenna << "\n";
                std::cout << "Points:\n";
                std::cout << "  (" << location.x << ", " << location.y << ")\n";
                std::cout << "  (" << location2.x << ", " << location2.y << ")\n";

                int x1 = location.x + (location.x - location2.x);
                int y1 = location.y + (location.y - location2.y);

                if (x1 >= 0 && x1 < width && y1 >= 0 && y1 < height)
                {
                    std::cout << "Anti-node:\n";
                    std::cout << "  (" << x1 << ", " << y1 << ")\n";
                    anti_nodes.insert(point{x1, y1});
                }

                int x2 = location2.x + (location2.x - location.x);
                int y2 = location2.y + (location2.y - location.y);

                if (x2 >= 0 && x2 < width && y2 >= 0 && y2 < height)
                {
                    std::cout << "Anti-node:\n";
                    std::cout << "  (" << x2 << ", " << y2 << ")\n";
                    anti_nodes.insert(point{x2, y2});
                }
            }
        }
    }
    return anti_nodes;
}