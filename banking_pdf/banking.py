import pdfminer.layout
from pdfminer.layout import LAParams, LTPage
from pdfminer.high_level import extract_pages
from typing import Dict, Iterator, List, Tuple

UPPER_ROW_BUFFER = 5
LOWER_ROW_BUFFER = 10

class bounding_box(object):
    """
    Used to specify the bounding box of a datum.
    """
    def __init__(self, x0: int=0, y0: int=0, x1: int=0, y1: int=0, datum: str="") -> None:
        self.datum = datum
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


# Correct the PDF file path using forward slashes or double backslashes
def main():
    
    
    pdf_path = '2023Sep.pdf'  # Adjust this path as necessary
    page_layouts = extract_pages(pdf_path)
    
    
    print(determine_columns(page_layouts))
    
    
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
    
    # result = determine_vertical_bounds(pdf_path, "jun")
    # left_x = 94.76400000000001
    # right_x = 252.48
    # for bottom_y, top_y in result:
    #     extract_text_by_coordinates(pdf_path, left_x, bottom_y, right_x, top_y)

# function to extract text box coordinates
def print_text_box_coordinates(pdf_path, search_term):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            # checking if the element is an instance of LTTextBoxHorizontal
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # printing the bounding box coordinates and text box
                text = element.get_text().strip()
                if search_term.lower() in text.lower():
                    print("---")
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

def determine_columns(page_layouts: Iterator[LTPage]) -> Dict[str, Tuple[float, float]]:
    """
    Goes through a Scotiabank pdf and extracts the x coordinates for columns.
    
    NOTE: Is hardcoded with magic numbers to work with the Scotiabank pdf format.
    
    args:
        page_layouts: an iterator of LTPage objects from pdfminer
    
    rtype:
        Dict[str, Tuple[float, float]]: a mapping of column names to a tuple of x0, x1 coordinates
    """
    columns = dict()
    for page_layout in page_layouts:
        for element in page_layout:
            # look for headers
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                text = element.get_text().strip()
                # transactions uses its own left x coord
                if "transactions" in text.lower():
                    try:
                        columns["transactions"] = (element.x0, columns["transactions"][1])
                    except KeyError:
                        columns["transactions"] = (element.x0, None)
                # transactions uses this right x coord
                elif "withdrawn" in text.lower():
                    columns["withdrawn"] = (element.x0, element.x1)
                    try:
                        columns["transactions"] = (columns["transactions"][0], element.x1)
                    except KeyError:
                        columns["transactions"] = (None, element.x1)
                elif "deposited" in text.lower():
                    columns["deposited"] = (element.x0, element.x1)
                elif "balance" in text.lower():
                    columns["balance"] = (element.x0, element.x1)
    
    return columns


def determine_rows(page_layouts: Iterator[LTPage], month: str) -> Dict[str, Tuple[float, float]]:
    """
    Goes through a Scotiabank pdf and extracts the y coordinates for rows.
    
    NOTE: Is hardcoded with magic numbers to work with the Scotiabank pdf format.
    
    args:
        page_layouts: an iterator of LTPage objects from pdfminer
        month: the three letter spelling of the month to search for
        
    rtype:
        Dict[str, Tuple[float, float]]: a mapping of row names (transaction dates) to a tuple of y0, y1 coordinates
    """
    # map transaction dates to raw y coord data
    rows = dict()
    
    for page_layout in page_layouts:
        # populate y coord data for each transaction date
        for element in page_layout:
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # look only for elments of the "Jan 30" or "Feb 1" form.
                text = element.get_text().strip()
                if len(text) <= 6 and month.lower() in text.lower():
                    rows[text] = (element.y0, element.y1)
                    
    return rows
                

def extract_transaction_data(file_path: str, columns: Dict[str, Tuple[float]], rows: Dict[str, Tuple[float, float]]) -> Dict[str, List[bounding_box]]:
    """
    Opens a Scotiabank pdf and extracts all the transaction data from the file.
    
    rtype:
        Dict[str, List[bounding_box]]: a mapping of dates to a list of bounding_box objects representing the transaction details
    """
    # map transaction dates to raw y coord data
    transactions = dict()
    
    for page_layout in page_layouts:
        # populate y coord data for each transaction date
        for element in page_layout:
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # look only for elments of the "Jan 30" or "Feb 1" form.
                text = element.get_text().strip()
                if len(text) <= 6 and month.lower() in text.lower():
                    transactions[text] = (element.y0, element.y1)
                    


if __name__ == '__main__':
    main()