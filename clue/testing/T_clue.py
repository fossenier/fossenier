import sys
import os

# Add the parent directory to sys.path to find the clue module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../fosstest/fosstest")
    )
)

from clue import pick_murderer, read_board
from testing_utilities import (
    assertion_error_raised,
    assertion_equality,
    assertion_list_content_equality,
)


def main() -> None:
    # setup constant to access the callables dynamically
    CALLABLES = {
        "c1": read_board,
        "c1_name": "read_board()",
        "c2": pick_murderer,
        "c2_name": "pick_murderer()",
    }
    ASSERTIONS = {
        "error_raised": assertion_error_raised,
        "equality": assertion_equality,
        "list_content_equality": assertion_list_content_equality,
    }

    # setup test suites to run through
    SUITES = {
        "c1": [
            {
                "assertion": "list_content_equality",
                "callable": "c1",
                "description": "read_board() happy path: valid small example.",
                "expected": (
                    [
                        [
                            "plum",
                        ],
                        [
                            "rope",
                        ],
                        [
                            "courtyard",
                        ],
                    ],
                ),
                "parameters": ("test-board2.csv",),
                "returns": True,
            },
            {
                "assertion": "list_content_equality",
                "callable": "c1",
                "description": "read_board() happy path: valid large example.",
                "expected": (
                    [
                        [
                            "plum",
                            " white",
                            " scarlet",
                            " green",
                            " mustard",
                            " peacock",
                        ],
                        [
                            "rope",
                            " dagger",
                            " wrench",
                            " pistol",
                            " candlestick",
                            " lead pipe",
                        ],
                        [
                            "courtyard",
                            " game room",
                            " study",
                            " dining room",
                            " garage",
                            " living room",
                            " kitchen",
                            " bedroom",
                            " bathroom",
                        ],
                    ],
                ),
                "parameters": ("test-board1.csv",),
                "returns": True,
            },
            {
                "assertion": "error_raised",
                "callable": "c1",
                "description": "read_board() unhappy path: invalid file format too few comments.",
                "expected": (ValueError,),
                "parameters": ("test-board3.csv",),
                "returns": True,
            },
            {
                "assertion": "error_raised",
                "callable": "c1",
                "description": "read_board() unhappy path: invalid path.",
                "expected": (ValueError,),
                "parameters": ("test-board-random-name.csv",),
                "returns": True,
            },
        ],
        "c2": [
            {
                "assertion": "equality",
                "callable": "c2",
                "description": "pick_murderer() happy path: one choice.",
                "expected": (["peacock", "rope", "courtyard"],),
                "parameters": (
                    ["peacock"],
                    ["rope"],
                    ["courtyard"],
                ),
                "returns": True,
            },
            {
                "assertion": "error_raised",
                "callable": "c2",
                "description": "pick_murderer() unhappy path: lack of choices.",
                "expected": (ValueError,),
                "parameters": (
                    ["peacock"],
                    ["rope"],
                    [],
                ),
                "returns": True,
            },
            {
                "assertion": "equality",
                "callable": "c2",
                "description": "pick_murderer() happy path: one choice, make sure original lists are modified.",
                "expected": ([],),
                "parameters": (
                    ["peacock"],
                    ["rope"],
                    ["courtyard"],
                ),
                "returns": False,
            },
        ],
    }

    # run each suite
    for suite_key in SUITES:

        # run each test
        for test in SUITES[suite_key]:
            assertion_key, callable_key, description, expected, parameters, returns = (
                test["assertion"],
                test["callable"],
                test["description"],
                test["expected"],
                test["parameters"],
                test["returns"],
            )
            # run the corresponding callable with the given parameters
            actual = None
            # catch and log errors as the result
            try:
                actual = CALLABLES[callable_key](*parameters)
            except ValueError as error:
                actual = type(error)
            # set the actual to be the initial object if we want to observe the initial parameter
            if not returns:
                actual = parameters[0]
            if not ASSERTIONS[assertion_key](actual, *expected):
                # print an informative message
                print(
                    f"FAIL   |   Potential error in case: `{description}`   |   Ran: {CALLABLES[callable_key + '_name']}   Parameters: {parameters}   Expected: {expected}   Actual: {actual} "
                )

    # give user feedback upon completion
    print("*** Test script completed ***")

    return


if __name__ == "__main__":
    main()
