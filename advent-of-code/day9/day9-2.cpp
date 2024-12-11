#include <fstream>
#include <iostream>

void compactMemory(std::vector<int> &memory);
void blockCompactMemory(std::vector<int> &memory, int fileCount);
long long int checkSum(std::vector<int> &memory);

int main()
{
    std::ifstream infile("day9.txt");
    if (!infile)
    {
        std::cerr << "File not found\n";
        return 1;
    }

    std::vector<int> memory;

    bool isFile{true};
    int fileCount{0};

    std::string line;
    if (std::getline(infile, line))
    {
        for (char c : line)
        {
            if (isdigit(c))
            {
                int number = c - '0';

                if (isFile)
                {
                    // Add the file count this many times
                    for (int i{0}; i < number; ++i)
                    {
                        memory.push_back(fileCount);
                    }
                    fileCount++;
                    isFile = false;
                }
                else
                {
                    // Add this many -1s to denote free space
                    for (int i{0}; i < number; ++i)
                    {
                        memory.push_back(-1);
                    }
                    isFile = true;
                }
            }
        }
    }

    for (int i : memory)
    {
        std::cout << i << ' ';
    }

    blockCompactMemory(memory, fileCount);

    for (int i{0}; i < 200; ++i)
    {
        std::cout << '\n';
    }

    std::cout << '\n';
    for (int i : memory)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';
    long long int result = checkSum(memory);

    std::cout << "Result: " << result << '\n';
}

/*

Given the memory, walks until finding a -1. Then, it will find the LAST file in
memory and swap it with the -1. This will compact the memory.

*/
void compactMemory(std::vector<int> &memory)
{
    for (int i{0}; i < memory.size(); ++i)
    {
        if (memory[i] == -1)
        {
            // Find the last file
            int lastFileIndex{0};
            for (int j{static_cast<int>(memory.size() - 1)}; j >= 0; --j)
            {
                // Memory is compacted
                if (j == i)
                {
                    return;
                }
                if (memory[j] != -1)
                {
                    lastFileIndex = j;
                    break;
                }
            }

            // Swap the last file with the -1
            int temp = memory[i];
            memory[i] = memory[lastFileIndex];
            memory[lastFileIndex] = temp;
        }
    }
}

/*

Given the memory, starts by going to the place in memory where there is the
fileCount number occurs (it will be a block of 1-9 consecutive numbers). Then,
try and fit these blocks in free spaces of -1, looking from the start. If it can't,
carry on to fileCount - 1.

*/
void blockCompactMemory(std::vector<int> &memory, int fileCount)
{
    for (int fileNum = fileCount - 1; fileNum >= 0; --fileNum)
    {
        // Find the block of the current fileNum
        std::vector<int> blockIndices;
        for (int j = 0; j < memory.size(); ++j)
        {
            if (memory[j] == fileNum)
            {
                blockIndices.push_back(j);
            }
        }

        // Try to fit this block into free spaces
        for (int k = 0; k < memory.size(); ++k)
        {
            // Abort if this would move the block to a higher index than it sits at
            if (k > blockIndices[0])
            {
                break;
            }

            if (memory[k] == -1)
            {
                bool canFit = true;
                for (int l = 0; l < blockIndices.size(); ++l)
                {
                    if (k + l >= memory.size() || memory[k + l] != -1)
                    {
                        canFit = false;
                        break;
                    }
                }

                if (canFit)
                {
                    for (int l = 0; l < blockIndices.size(); ++l)
                    {
                        memory[k + l] = fileNum;
                        memory[blockIndices[l]] = -1;
                    }
                    break;
                }
            }
        }
    }
}

long long int checkSum(std::vector<int> &memory)
{
    long long int sum{0};

    for (int i{0}; i < memory.size(); ++i)
    {
        if (memory[i] == -1)
        {
            continue;
        }
        sum += memory[i] * i;
    }

    return sum;
}