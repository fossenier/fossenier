from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal

from typing import Dict, Iterator, List, Tuple

import datetime

"""
Attempt 2 at reading Scotiabank PDF statements
"""

MONTHS = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def main():
    pdf_path = "2023Sep.pdf"  # Adjust this path as necessary
    file_path = "private.csv"  # Adjust this path as necessary
    layouts = read_pages(pdf_path)

    dates_rows, year = determine_rows(layouts)
    # print(dates_rows)

    headers_columns = determine_columns(layouts)
    # print(headers_columns)

    transactions = populate_transactions(layouts, dates_rows, headers_columns)
    # print(transactions)

    store_transactions(file_path, transactions, year)


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
                    raw_time = text.split(" ")
                    raw_month = raw_time[3]
                    year = raw_time[5]
                    month = raw_month[:3].lower()
                # find all instances of "Jan 30" or "Feb 1" etc. as these mark transactions
                elif month and month in text.lower() and len(text) <= 6:
                    rows[text] = (element.y0, element.y1)

    return rows, year


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
                                transactions[date][column] = text.strip()
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


def store_transactions(
    file_path: str, transactions: Dict[str, Dict[str, str]], year: str
):
    """
    Stores the transactions in a CSV file.

    args:
        file_path: str - the path to the CSV file
        transactions: Dict[str, Dict[str, str]] - the transactions
    """
    with open(file_path, "w") as file:
        # put the right columns for the Monarch format
        file.write(
            "date,merchant,category,account,original statement,notes,amount,tags\n"
        )

        # sort by date and pull the transaction data
        for date, transaction in sorted(
            transactions.items(),
            key=lambda x: datetime.datetime.strptime(f"{x[0]} {year}", "%b %d %Y"),
        ):
            # Ignore the opening balance and closing balance
            if transaction["transactions"].lower() in [
                "opening balance",
                "closing balance",
            ]:
                continue

            # there may be a statement and a "merchant", or just a "merchant"
            if "\n" in transaction["transactions"]:
                statement, merchant = transaction["transactions"].split("\n")
            else:
                statement = transaction["transactions"]
                merchant = transaction["transactions"]

            # format the date as "2024-01-30"
            month, day = date.split(" ")
            date = f"{year}-{MONTHS[month.lower()]}-{day}"

            # the amount exists and is positive
            if transaction["deposited"]:
                amount = transaction["deposited"].replace(",", "")
            # the amount exists and is negative
            elif transaction["withdrawn"]:
                amount = f"-{transaction['withdrawn'].replace(',', '')}"
            else:
                amount = "0.00"

            file.write(f"{date},{merchant},,,{statement},,{amount},\n")


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
