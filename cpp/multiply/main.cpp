#include <iostream>

int main()
{
    // let user choose base
    std::cout << "Please enter an integer: ";

    int num{};
    std::cin >> num; // store base

    std::cout << num * 2 << '\n'; // print the double
    return 0;
}