#include <fstream>
#include <iostream>
#include <sstream>

bool validUpdate(std::vector<std::vector<int>> all_rules, std::vector<int> numbers);
int reorder(std::vector<std::vector<int>> all_rules, std::vector<int> numbers);

int main()
{
    std::ifstream infile("day5.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<std::vector<int>> all_rules;

    std::string line{};
    while (std::getline(infile, line))
    {
        // Stop on an empty line
        if (line.empty())
        {
            break;
        }

        std::vector<int> rule{};
        std::istringstream iss(line);
        std::string num;
        while (std::getline(iss, num, '|'))
        {
            rule.push_back(std::stoi(num));
        }
        all_rules.push_back(rule);
    }

    long middles_count{0};

    while (std::getline(infile, line))
    {
        std::vector<int> numbers;
        std::istringstream iss(line);
        std::string num;
        while (std::getline(iss, num, ','))
        {
            numbers.push_back(std::stoi(num));
        }

        // Check if the number is valid
        if (validUpdate(all_rules, numbers))
        {
            continue;
        }
        else
        {
            middles_count += reorder(all_rules, numbers);
        }
    }
    infile.close();

    std::cout << "Summation: " << middles_count << '\n';
}

bool validUpdate(std::vector<std::vector<int>> all_rules, std::vector<int> numbers)
{
    // Given a list of numbers, each [0] in one rule must always occur before the [1] in the same rule
    // If this fails for even one rule, return false. Otherwise, return true
    for (auto rule : all_rules)
    {
        // This should not trigger if [1] cannot be found, or if [0] cannot be found
        auto pos0 = std::find(numbers.begin(), numbers.end(), rule[0]);
        auto pos1 = std::find(numbers.begin(), numbers.end(), rule[1]);
        if (pos0 == numbers.end() || pos1 == numbers.end())
        {
            continue;
        }
        else if (pos0 > pos1)
        {
            return false;
        }
    }
    return true;
}

int reorder(std::vector<std::vector<int>> all_rules, std::vector<int> numbers)
{
    // The below is failing to make the numbers adhere to the rules. It should try again and
    // again until the rules are met. If the rules are never met, return 0

    // Given a list of numbers, reorder them so that each [0] in one rule occurs before the [1] in the same rule
    // If this fails for even one rule, return 0. Otherwise, return the middle number AKA numbers[numbers.size() / 2]
    bool reordered = true;
    do
    {
        reordered = false;
        for (auto rule : all_rules)
        {
            auto pos0 = std::find(numbers.begin(), numbers.end(), rule[0]);
            auto pos1 = std::find(numbers.begin(), numbers.end(), rule[1]);
            if (pos0 == numbers.end() || pos1 == numbers.end())
            {
                continue;
            }
            else if (pos0 > pos1)
            {
                std::iter_swap(pos0, pos1);
                reordered = true;
            }
        }
    } while (reordered);

    for (auto rule : all_rules)
    {
        auto pos0 = std::find(numbers.begin(), numbers.end(), rule[0]);
        auto pos1 = std::find(numbers.begin(), numbers.end(), rule[1]);
        if (pos0 == numbers.end() || pos1 == numbers.end())
        {
            continue;
        }
        else if (pos0 > pos1)
        {
            return 0;
        }
    }
    return numbers[numbers.size() / 2];
}