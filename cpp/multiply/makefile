# Flags to be passed to the g++ compiler
CXXFLAGS = -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -Werror -std=c++20

# The compiler to use
CXX = g++

# Target 'all' depends on 'program'
all: program

# 'program' depends on 'main.o'. Link the object files into an executable
program: main.o
	$(CXX) $(CXXFLAGS) main.o -o program

# 'main.o' depends on 'main.cpp'. Compile the source files into object files
main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp

# Clean up binary files. This doesn't produce a file named 'clean', so it's a phony target
clean:
	rm -f *.o program
