#include <fstream>
#include <iostream>
#include <set>
#include <vector>

long int tallyCost(std::vector<std::vector<char>> &plot_map,
                   std::set<char> &plot_types);
int tallyField(std::vector<std::vector<char>> &plot_map,
               std::set<std::pair<int, int>> &visited,
               char type, int row, int col);

int main()
{
    std::ifstream infile("day12.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::set<char> plot_types;
    std::vector<std::vector<char>> plot_map;

    std::string line;
    while (std::getline(infile, line))
    {
        std::vector<char> row;

        for (char c : line)
        {
            row.push_back(c);
            plot_types.insert(c);
        }

        plot_map.push_back(row);
    }

    long int result{tallyCost(plot_map, plot_types)};
    std::cout << "Result: " << result << '\n';
}

long int tallyCost(std::vector<std::vector<char>> &plot_map,
                   std::set<char> &plot_types)
{
    long int cost{0};
    std::set<std::pair<int, int>> visited;
    // For each plot type
    for (const char &type : plot_types)
    {
        for (int row{0}; row < plot_map.size(); row++)
        {
            for (int col{0}; col < plot_map[row].size(); col++)
            {
                // If the plot has been visited, skip it
                if (visited.find({row, col}) != visited.end())
                {
                    continue;
                }

                if (plot_map[row][col] == type)
                {
                    cost += tallyField(plot_map, visited, type, row, col);
                }
            }
        }
    }
    return cost;
}

int tallyField(std::vector<std::vector<char>> &plot_map,
               std::set<std::pair<int, int>> &visited,
               char type, int first_row, int first_col)
{
    int area{0};
    int perimeter{0};

    std::vector<std::pair<int, int>> frontier; // Will always have valid points
    visited.insert({first_row, first_col});
    frontier.push_back({first_row, first_col});

    while (!frontier.empty())
    {
        std::pair<int, int> current = frontier.back();
        frontier.pop_back();

        area++;

        int row{current.first};
        int col{current.second};

        for (int i{-1}; i <= 1; i++)
        {
            for (int j{-1}; j <= 1; j++)
            {
                // Skip the current point and the diagonals
                if ((i == 0 && j == 0) || (i != 0 && j != 0))
                {
                    continue;
                }

                int new_row{row + i};
                int new_col{col + j};

                if (new_row < 0 || new_row >= plot_map.size() || new_col < 0 || new_col >= plot_map[new_row].size())
                {
                    perimeter++;
                    continue;
                }
                else if (plot_map[new_row][new_col] != type)
                {
                    perimeter++;
                    continue;
                }

                if (visited.find({new_row, new_col}) == visited.end())
                {
                    visited.insert({new_row, new_col});
                    frontier.push_back({new_row, new_col});
                }
            }
        }
    }
    std::cout << "Type: " << type << " Area: " << area << " Perimeter: " << perimeter << '\n';
    return area * perimeter;
}