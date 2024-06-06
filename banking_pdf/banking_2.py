from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal

from typing import Dict, Iterator, List, Tuple

"""
Attempt 2 at reading Scotiabank PDF statements
"""


def main():
    pdf_path = "2023Sep.pdf"  # Adjust this path as necessary
    page_layouts = list(extract_pages(pdf_path))
    stringent_layouts = stringent_read(pdf_path)

    dates_rows = determine_rows(stringent_layouts)
    print(dates_rows)

    headers_columns = determine_columns(page_layouts)
    print(headers_columns)


def determine_columns(page_layouts: List[LTPage]) -> Dict[str, Tuple[float, float]]:
    """
    Determines the columns in the PDF.

    args:
        page_layouts: List[LTPage] - the pages of the PDF (allow multi line textboxes)

    rtype:
        Dict[str, Tuple[float, float]] - a dictionary with the column name as the key, and the x0 and x1 as the value.
    """
    columns = dict()
    for page_layout in page_layouts:
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                if text.lower() == "date":
                    columns["date"] = (element.x0, element.x1)
                elif text.lower() == "transaction":
                    columns["transaction"] = (element.x0, element.x1)
                elif text.lower() == "withdrawn":
                    columns["withdrawn"] = (element.x0, element.x1)
                elif text.lower() == "deposited":
                    columns["deposited"] = (element.x0, element.x1)
                elif text.lower() == "balance":
                    columns["balance"] = (element.x0, element.x1)

    return columns


def determine_rows(page_layouts: List[LTPage]) -> Dict[str, Tuple[float, float]]:
    """
    Determines the transaction rows in the PDF.

    args:
        page_layouts: List[LTPage] - the pages of the PDF (be stringent)

    rtype:
        Dict[str, Tuple[float, float]] - a dictionary with the date as the key, and the y0 and y1 as the value.
    """
    rows = dict()
    month = None

    for page_layout in page_layouts:
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # grab the month as "feb", "mar", etc.
                if "opening balance on " in text.lower():
                    raw_month = text.split(" ")[3]
                    month = raw_month[:3].lower()
                # find all instances of "Jan 30" or "Feb 1" etc. as these mark transactions
                elif month and month in text.lower() and len(text) <= 6:
                    rows[text] = (element.y0, element.y1)

    return rows


def stringent_read(pdf_path: str) -> List[LTPage]:
    """
    Reads the PDF file with stringent LAParams.
    Disables multi line, and makes text need to be closer together.

    Great for reading dates, and withdrawals/deposits.
    """
    line_margin = -1  # do not allow multi line textboxes
    char_margin = 1.2  # shrink the default to require words being closer
    laparams = LAParams(
        char_margin=char_margin, line_margin=line_margin, detect_vertical=False
    )

    return list(extract_pages(pdf_path, laparams=laparams))


if __name__ == "__main__":
    main()
