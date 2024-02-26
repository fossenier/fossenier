import io
import sys
from wordsfornumbers import (
    main,
)  # Make sure to replace 'your_program_file' with the name of your Python file containing the code.


# A wrapper function to capture the output of main()
def run_test(inputs):
    # Backup the original stdin and stdout
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Replace stdin and stdout with StringIO objects to simulate input and capture output
    sys.stdin = io.StringIO("\n".join(inputs) + "\n")
    sys.stdout = io.StringIO()

    # Run the main function
    main()

    # Capture the output, then revert stdin and stdout to their original objects
    output = sys.stdout.getvalue()
    sys.stdin = original_stdin
    sys.stdout = original_stdout

    # Split the output by lines and return the list
    return output.strip().split("\n")


# Example test cases
test_inputs = [
    "I have 2 apples and 3 oranges",
    "She is 19 years old",
    "In the year 2020, many events happened",
]

expected_outputs = [
    "I have two apples and three oranges",
    "She is nineteen years old",
    "In the year twenty twenty, many events happened",
]

# Run the test
actual_outputs = run_test(test_inputs)

# Check if the actual outputs match the expected outputs
for i, (actual, expected) in enumerate(zip(actual_outputs, expected_outputs)):
    assert (
        actual == expected
    ), f"Test case {i+1} failed: expected '{expected}', got '{actual}'"

print("All tests passed!")
