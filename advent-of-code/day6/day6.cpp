#include <fstream>
#include <iostream>
#include <sstream>

bool checkLoopPathFind(std::vector<std::vector<char>> &map, int row, int col);
void printMap(const std::vector<std::vector<char>> &map);
int simulateObstruction(std::vector<std::vector<char>> &map, int row, int col);

int main()
{
    std::ifstream infile("day6.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<std::vector<char>> map;

    // Store the starding coords
    int row{0};
    int col{0};

    int current_row{0};
    int current_col{0};

    std::string line{};
    while (std::getline(infile, line))
    {
        // Break each line into a vector of characters
        current_col = 0;
        std::vector<char> char_row{};
        for (char c : line)
        {
            if (c == '^')
            {
                row = current_row;
                col = current_col;
                c = 'X';
            }
            current_col++;
            char_row.push_back(c);
        }
        current_row++;
        map.push_back(char_row);
    }

    // We now have a 2D array of characters
    std::cout << "Starting at: " << row << ", " << col << '\n';

    printMap(map);

    std::cout << "Count: " << simulateObstruction(map, row, col) << '\n';
}

/*
This function will track the number of steps taken, and return true if it has stepped
more than the area of the map. This is a sign that the player is stuck in a loop.
*/
bool checkLoopPathFind(std::vector<std::vector<char>> &map, int row, int col)
{
    int steps{0};

    // The player is facing up
    char direction = '^';

    // The player is at the starting position
    int current_row = row;
    int current_col = col;

    // The player is not done
    bool done = false;

    // The player will move in the direction it is facing
    while (!done)
    {
        // Pick where the player will step
        switch (direction)
        {
        case '^':
            current_row--;
            break;
        case '>':
            current_col++;
            break;
        case 'v':
            current_row++;
            break;
        case '<':
            current_col--;
            break;
        }

        // If the player is out of bounds, stop
        if (current_row < 0 || current_row >= map.size() || current_col < 0 || current_col >= map[current_row].size())
        {
            done = true;
            break;
        }

        // If the player will hit a wall, turn right
        if (map[current_row][current_col] == '#')
        {
            switch (direction)
            {
            case '^':
                direction = '>';
                current_row++;
                break;
            case '>':
                direction = 'v';
                current_col--;
                break;
            case 'v':
                direction = '<';
                current_row--;
                break;
            case '<':
                direction = '^';
                current_col++;
                break;
            }
        }

        // If the player is at an open space, move forward
        else if (map[current_row][current_col] == '.')
        {
            map[current_row][current_col] = 'X';
        }
        steps++;

        // If the player has taken more steps than the area of the map, it is stuck in a loop
        if (steps > map.size() * map[0].size())
        {
            return true;
        }
    }
}

void printMap(const std::vector<std::vector<char>> &map)
{
    for (int row{0}; row < map.size(); ++row)
    {
        for (int col{0}; col < map[row].size(); ++col)
        {
            std::cout << map[row][col];
        }
        std::cout << '\n';
    }
}

/*

This function will simulate one obstruction being placed at every tile on the map.
It will then check if that will create a loop. If it does, it will tally that result.

It should then return that tile to the previous state, it will never place an obstruction
at the starting row and column.

*/
int simulateObstruction(std::vector<std::vector<char>> &map, int row, int col)
{
    int count{0};

    for (int r{0}; r < map.size(); ++r)
    {
        for (int c{0}; c < map[r].size(); ++c)
        {
            if (r == row && c == col)
            {
                continue;
            }

            // Save the current state of the map
            char temp = map[r][c];

            // Place an obstruction
            map[r][c] = '#';

            // Check if the player is stuck in a loop
            if (checkLoopPathFind(map, row, col))
            {
                count++;
            }

            std::cout << "Ran test, total: " << count << '\n';

            // Return the map to its previous state
            map[r][c] = temp;
        }
    }

    return count;
}