from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal

from typing import Dict, Iterator, List, Tuple

"""
Attempt 2 at reading Scotiabank PDF statements
"""


def main():
    pdf_path = "2023Sep.pdf"  # Adjust this path as necessary
    layouts = read_pages(pdf_path)

    dates_rows = determine_rows(layouts)
    print(dates_rows)

    headers_columns = determine_columns(layouts)
    print(headers_columns)

    transactions = populate_transactions(layouts, dates_rows, headers_columns)
    print(transactions)


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
                if "transactions" in text.lower():
                    columns["transactions"] = (element.x0, element.x1)
                elif "withdrawn" in text.lower():
                    columns["withdrawn"] = (element.x0, element.x1)
                elif "deposited" in text.lower():
                    columns["deposited"] = (element.x0, element.x1)

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


def populate_transactions(
    layouts: List[LTPage],
    dates_rows: Dict[str, Tuple[float, float]],
    headers_columns: Dict[str, Tuple[float, float]],
):
    """
    Populates the transactions from the PDF.

    args:
        layouts: List[LTPage] - the pages of the PDF
        dates_rows: Dict[str, Tuple[float, float]] - the date rows
        headers_columns: Dict[str, Tuple[float, float]] - the columns

    rtype:
        None
    """
    transactions = dict()

    # TODO cleanup this magic number
    SPACER = 5
    for page_layout in layouts:
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # this is a correct row
                for date, (y0, y1) in dates_rows.items():
                    if y0 - (SPACER * 2) < element.y0 < y1 + SPACER:
                        # create the transaction if it doesn't exist
                        try:
                            transactions[date]
                        except KeyError:
                            transactions[date] = {
                                "transactions": None,
                                "withdrawn": None,
                                "deposited": None,
                            }
                        # this is a valid column for the row
                        for column, (x0, x1) in headers_columns.items():
                            if x0 - SPACER < element.x0 < x1 + SPACER:
                                # populate the transaction
                                transactions[date][column] = text
    return transactions


def read_pages(pdf_path: str) -> List[LTPage]:
    """
    Reads the PDF file with LAParams tailored for Scotiabank PDFs.
    Allows multi line and forces sentences to require text closer together.

    args:
        pdf_path: str - the path to the PDF file

    rtype:
        List[LTPage] - the pages of the PDF
    """
    line_margin = 0.3  # allow multi line textboxes
    char_margin = 1.2  # shrink the default to require words being closer
    laparams = LAParams(
        char_margin=char_margin, line_margin=line_margin, detect_vertical=True
    )

    # TODO remove
    # for page_layout in extract_pages(pdf_path, laparams=laparams):
    #     for element in page_layout:
    #         if isinstance(element, LTTextBoxHorizontal):
    #             print("---")
    #             print(element.get_text().strip())

    return list(extract_pages(pdf_path, laparams=laparams))


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
