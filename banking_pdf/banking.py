import pdfminer.layout
from pdfminer.high_level import extract_pages

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
    print(result)

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
                    print(element.get_text())


def determine_vertical_bounds(pdf_path, month):
    """
    Given the three letter spelling of a month, reads a Scotiabank pdf and fetches
    all the transactions of that month. For each transaction on the pdf, this function
    will create an entry in a dictionary keyed from '-1' to 'len(transactions) + 1'
    and will populate a bounding_box() object as each value.
    
    The top of each bounding box will be the bottom of the previous transaction, and the
    bottom of each bounding box will be the top of the next transaction. Thus, the first
    and last transactions will not be recorded, and the first, second, last, and second
    last entries in the dictionary will be removed before being returned.
    """
    # initialize a counter to track and entries and the dictionary for the entries
    discovered_entries = 0
    vertical_bounds = dict()
    
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            # checking if the element is an instance of LTTextBoxHorizontal
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                # save the coords should it be a date
                text = element.get_text().strip()
                if month.lower() in text.lower() and len(text) <= 6:
                    prev_entry = str(discovered_entries - 1)
                    entry = str(discovered_entries)
                    next_entry = str(discovered_entries + 1)
                    
                    discovered_entries += 1
                    
                    # set the top right y coord of the next entry corresponding to the
                    # bottom of this entry
                    try:
                        vertical_bounds[prev_entry].top_right[1] = element.y0
                    except KeyError:
                        vertical_bounds[prev_entry] = bounding_box(y1=element.y0)
                    # capture the date of this entry
                    try:
                        vertical_bounds[entry].date = text
                    except KeyError:
                        vertical_bounds[entry] = bounding_box(date=text)
                    # set the bottom left y coord of the previous entry corresponding
                    # to the top of this entry
                    try:
                        vertical_bounds[next_entry].bottom_left[1] = element.y1
                    except KeyError:
                        vertical_bounds[next_entry] = bounding_box(y0=element.y1)
    return vertical_bounds

if __name__ == '__main__':
    main()