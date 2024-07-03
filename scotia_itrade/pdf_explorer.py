"""
Prints out informative pdf data to determine routes of mining.
"""

from datetime import datetime
from typing import Iterator
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages


def main() -> None:
    """
    Opens a PDF file and reads the pages.
    """
    # print a big notable block to the command line
    for _ in range(14):
        print("!" * 80)
    path = "fund6.pdf"

    # print_content(path, True)
    search_content(path, True)


def search_content(path: str, locations: bool = False) -> None:
    """
    Searches the content of the PDF file.

    args:
        path: str - the path to the PDF file
    """
    text = None
    while text != "":
        text = input("Enter the text to search for: ")
        for page_layout in read_pages(path):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    if text in element.get_text():
                        print()
                        print(element.get_text())
                        if locations:
                            print(
                                f"x0: {element.x0}, x1: {element.x1}, y0: {element.y0}, y1: {element.y1}"
                            )


def print_content(path: str, locations: bool = False) -> None:
    """
    Prints the content of the PDF file.

    args:
        path: str - the path to the PDF file
    """
    for page_layout in read_pages(path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                print()
                print(text)
                if locations:
                    print(
                        f"x0: {element.x0}, x1: {element.x1}, y0: {element.y0}, y1: {element.y1}"
                    )


def read_pages(path: str) -> Iterator[LTPage]:
    """
    Reads the PDF file with LAParams.
    Allows multi line and forces sentences to require text closer together.

    args:
        path: str - the path to the PDF file

    rtype:
        Iterator[LTPage] - the pages of the PDF
    """
    line_margin = 0.3  # allow multi line textboxes
    char_margin = 1.2  # shrink the default to require words being closer
    laparams = LAParams(char_margin=char_margin, line_margin=line_margin)

    for page_layout in extract_pages(path, laparams=laparams):
        yield page_layout


if __name__ == "__main__":
    main()
