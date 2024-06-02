import pdfminer.layout
from pdfminer.high_level import extract_pages
from typing import Tuple

UPPER_ROW_BUFFER = 5
LOWER_ROW_BUFFER = 10

class bounding_box(object):
    """
    Used to specify the bounding box of a specific entry.
    """
    def __init__(self, x0=0, y0=0, x1=0, y1=0, date=""):
        self.bottom_left = [x0, y0]
        self.top_right = [x1, y1]
        self.date = date


# Correct the PDF file path using forward slashes or double backslashes
def main():
    
    
    
    pdf_path = '2018Jun.pdf'  # Adjust this path as necessary
    # search_term = None
    # while True:
    #     search_term = input("Enter the search term: ")
    #     if search_term == "!stop":
    #         break
    #     elif search_term == "!path": 
    #         pdf_path = input("Enter the PDF file path: ")
    #     print_text_box_coordinates(pdf_path, search_term)
    
    # defx = 99.76
    # gx = 252.48
    # fy = 323.082
    # ay = 358.002
    # extract_text_by_coordinates(pdf_path, defx, fy, gx, ay)
    
    result = determine_vertical_bounds(pdf_path, "jun")
    left_x = 94.76400000000001
    right_x = 252.48
    for bottom_y, top_y in result:
        extract_text_by_coordinates(pdf_path, left_x, bottom_y, right_x, top_y)

# function to extract text box coordinates
def print_text_box_coordinates(pdf_path, search_term):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            # checking if the element is an instance of LTTextBoxHorizontal
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # printing the bounding box coordinates and text box
                text = element.get_text().strip()
                if search_term.lower() in text.lower():
                    print(f"Text Box: {text}")
                    print(f"Coordinates: ({element.x0}, {element.y0}, {element.x1}, {element.y1})")
                    print("---")  # separator for readability

# Function to extract text
def extract_text_by_coordinates(pdf_path, x0, y0, x1, y1):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # Check if the text box is within the specified coordinates
                if (x0 <= element.x0 and element.x1 <= x1 and
                    y0 <= element.y0 and element.y1 <= y1):
                    print(element.get_text().strip())


def determine_vertical_bounds(pdf_path, month: str) -> Tuple[float, float]:
    """
    Given the three letter spelling of a month, reads a Scotiabank pdf and fetches
    all the transactions of that month.
    
    Returns a (lower_y_coord, upper_y_coord) tuple for each transaction.
    """
    transaction_y_bounds = []
    
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # match the element to the "Jan 14" or "Jun 30" format
                text = element.get_text().strip()
                if len(text) <= 6 and month.lower() in text.lower():
                    # use the row buffer to make sure the larger Transaction column entry
                    # is included in the bounds given by the smaller Date column entry
                    transaction_y_bounds.append((element.y0 - LOWER_ROW_BUFFER, element.y1 + UPPER_ROW_BUFFER))
                    
    return transaction_y_bounds


if __name__ == '__main__':
    main()