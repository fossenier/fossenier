#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <future>
#include <mutex> // Add this header for std::mutex

void blink(std::vector<long int> &stones, size_t start, size_t end, std::vector<long int> &result);

std::mutex mutex; // Define the mutex to be used for thread synchronization

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

    int iterations = 75; // Specify iterations
    std::vector<long int> stones_copy = stones;

    // Parallelize the iterations over the blink function
    for (int i = 0; i < iterations; i++)
    {
        std::vector<std::future<void>> futures;
        size_t chunk_size = stones_copy.size() / std::thread::hardware_concurrency();

        // Split the work into chunks and create threads
        for (size_t j = 0; j < std::thread::hardware_concurrency(); ++j)
        {
            size_t start = j * chunk_size;
            size_t end = (j == std::thread::hardware_concurrency() - 1) ? stones_copy.size() : (j + 1) * chunk_size;

            // Create a future for each thread
            futures.push_back(std::async(std::launch::async, blink, std::ref(stones_copy), start, end, std::ref(stones_copy)));
        }

        // Wait for all threads to finish
        for (auto &f : futures)
        {
            f.get();
        }
    }

    std::cout << "Processing complete.\n";

    return 0;
}

void blink(std::vector<long int> &stones, size_t start, size_t end, std::vector<long int> &result)
{
    std::vector<long int> local_result;
    local_result.reserve(stones.size() * 2); // Reserve enough memory to avoid reallocations

    for (size_t i = start; i < end; i++)
    {
        long int stone = stones[i];
        if (stone == 0)
        {
            local_result.push_back(1);
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

            local_result.push_back(std::stol(first_half));
            local_result.push_back(std::stol(second_half));
        }
        else
        {
            local_result.push_back(stone * 2024);
        }
    }

    // Synchronize the result (e.g., appending to the main vector)
    std::lock_guard<std::mutex> guard(mutex);
    result.insert(result.end(), local_result.begin(), local_result.end());
}
