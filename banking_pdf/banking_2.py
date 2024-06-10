"""
Reads Scotiabank PDF statements and outputs a CSV file in Monarch format.
"""

from datetime import datetime
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from typing import Dict, Iterator, List, Tuple

# keys for the transactions dictionary
DEPOSIT = "deposit"
TRANSACTION = "transaction"
WITHDRAWAL = "withdrawal"


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
    Determines the columns in a Scotiabank monthly statement PDF. Transactions, withdrawals, and deposits.

    args:
        page_layouts: List[LTPage] - the pages of the PDF

    rtype:
        Dict[str, Tuple[float, float]] - a dictionary with the column constants as the key, and the x0 and x1 as the value.
    """
    # exactly what the columns are called in the PDF
    transaction = "Transactions"
    withdrawal = "Amounts\nwithdrawn ($)"
    deposit = "Amounts\ndeposited ($)"
    
    columns = dict()
    for page_layout in page_layouts:
        for element in page_layout:
            # save coordinates for the desired columns
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # exact match for the column names
                if transaction == text:
                    columns[TRANSACTION] = (element.x0, element.x1)
                elif withdrawal == text:
                    columns[WITHDRAWAL] = (element.x0, element.x1)
                elif deposit == text:
                    columns[DEPOSIT] = (element.x0, element.x1)

    return columns


def determine_rows(page_layouts: List[LTPage]) -> Tuple[Dict[str, Tuple[float, float]], str]:
    """
    Determines the rows of transactions in a Scotiabank monthly statement PDF.

    args:
        page_layouts: List[LTPage] - the pages of the PDF

    rtype:
        Tuple[Dict[str, Tuple[float, float]], str] - a dictionary with each transaction date as the key,
        mapped to the y0 and y1 of the transaction row, as well as the year
    """
    # exactly what the month containing textbox starts with
    opening_balance = "Opening Balance on "
    
    # the rows to be returned
    rows = dict()
    # the month and year of the statement
    month = None
    year = None

    for page_layout in page_layouts:
        for element in page_layout:
            # save coordinates for the desired rows
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # grab the month as "feb", "mar", etc. from the one specific textbox
                # the first clause is to save computation
                if not month and text.startswith(opening_balance):
                    raw_time = text.split(" ")
                    raw_month = raw_time[3]
                    # collect the year
                    year = raw_time[5]
                    month = raw_month[:3]
                # find all instances of "Jan 30" or "Feb 1" etc. as these mark transactions
                # the len() check is to avoid usage of the month in a textbox where it's not a transaction
                elif month and text.startswith(month) and len(text) <= 6:
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
                                TRANSACTION: None,
                                WITHDRAWAL: None,
                                DEPOSIT: None,
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
            key=lambda x: datetime.strptime(f"{x[0]} {year}", "%b %d %Y"),
        ):
            # Ignore the opening balance and closing balance
            if transaction[TRANSACTION].lower() in [
                "opening balance",
                "closing balance",
            ]:
                continue

            # there may be a statement and a "merchant", or just a "merchant"
            if "\n" in transaction[TRANSACTION]:
                statement, merchant = transaction[TRANSACTION].split("\n")
            else:
                statement = transaction[TRANSACTION]
                merchant = transaction[TRANSACTION]

            # format the date as "2024-01-30"
            month, day = date.split(" ")
            formatted_date = datetime.strptime(
                f"{month} {day} {year}", "%b %d %Y"
            ).strftime("%Y-%m-%d")

            # the amount exists and is positive
            if transaction[DEPOSIT]:
                amount = transaction[DEPOSIT].replace(",", "")
            # the amount exists and is negative
            elif transaction[WITHDRAWAL]:
                amount = f"-{transaction[WITHDRAWAL].replace(",", "")}"
            else:
                amount = "0.00"

            file.write(f"{formatted_date},{merchant},,,{statement},,{amount},\n")


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