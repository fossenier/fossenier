"""
Reads Scotiabank PDF statements and outputs a CSV file in Monarch format.
"""

from csv import DictReader, DictWriter
from datetime import datetime
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from typing import Dict, Iterator, List, Tuple

import os

# keys for the transactions dictionary
DEPOSIT = "deposit"
TRANSACTION = "transaction"
WITHDRAWAL = "withdrawal"


def main():
    # WARNING no touchy: my .gitignore is set to ignore this file
    output_path = "private.csv"
    target_directory = os.getcwd()

    # create the output CSV
    with open(output_path, "w") as file:
        # put the right columns for the Monarch format
        file.write(
            "date,merchant,category,account,original statement,notes,amount,tags\n"
        )

    pdf_paths = []
    # walk through all directories and subdirectories
    for dirpath, _, filenames in os.walk(target_directory):
        for filename in filenames:
            # save Scotiabank PDF paths
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(dirpath, filename)
                pdf_paths.append(pdf_path)

    # extract all transactions from each PDF
    for path in pdf_paths:

        page_layouts = read_pages(path)
        dates_rows, year = determine_rows(page_layouts)
        headers_columns = determine_columns(page_layouts)
        transactions = populate_transactions(page_layouts, dates_rows, headers_columns)
        store_transactions(output_path, transactions, year)


def determine_columns(page_layouts: List[LTPage]) -> Dict[str, Tuple[float, float]]:
    """
    Determines the columns in a Scotiabank monthly statement PDF. Transactions, withdrawals, and deposits.

    args:
        page_layouts: List[LTPage] - the pages of the PDF

    rtype:
        Dict[str, Tuple[float, float]] - a dictionary with the column constants as the key, and the x0
        and x1 as the value.
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


def determine_rows(
    page_layouts: List[LTPage],
) -> Tuple[Dict[str, Tuple[float, float]], str]:
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
    page_layouts: List[LTPage],
    dates_rows: Dict[str, Tuple[float, float]],
    headers_columns: Dict[str, Tuple[float, float]],
) -> Dict[str, Dict[str, str]]:
    """
    Populates a Scotiabank monthly statement PDF into memory using pre-determined search areas.

    args:
        page_layouts: List[LTPage] - the pages of the PDF
        dates_rows: Dict[str, Tuple[float, float]] - a dictionary with each transaction date
        as the key, mapped to the y0 and y1 of the transaction row
        headers_columns: Dict[str, Tuple[float, float]] - a dictionary with the column
        constants as the key, and the x0 and x1 as the value.

    rtype:
        Dict[str, Dict[str, str]] - a dictionary with each transaction date as the key, mapped to
        the transaction, withdrawal, and deposit as the value
    """
    # define a window of space around the textboxes to allow for some error
    GRACE = 5
    # the transactions to be returned
    transactions = dict()

    for page_layout in page_layouts:
        for element in page_layout:
            # save the text in the correct row and column
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # this is a correct row
                for date, (y0, y1) in dates_rows.items():
                    if y0 - (GRACE * 2) < element.y0 < y1 + GRACE:
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
                        for header, (x0, x1) in headers_columns.items():
                            if x0 - GRACE < element.x0 < x1 + GRACE:
                                # populate the transaction
                                transactions[date][header] = text.strip()
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

    # make into a list to allow for repeated use, but takes up more memory
    return list(extract_pages(pdf_path, laparams=laparams))


def store_transactions(
    file_path: str, transactions: Dict[str, Dict[str, str]], year: str
):
    """
    Stores the transactions in a CSV file by appending them in chronological order.
    Assume Monarch data is already present and needs to be kept in order.

    args:
        file_path: str - the path to the CSV file
        transactions: Dict[str, Dict[str, str]] - the transactions
        year: str - the year of the statement
    """
    # read existing data from CSV
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = DictReader(file)
        existing_data = [row for row in reader]

    # append new data with the correct formatting
    for date, transaction in transactions.items():
        if transaction[TRANSACTION].lower() in ["opening balance", "closing balance"]:
            continue
        if "\n" in transaction[TRANSACTION]:
            statement, merchant = transaction[TRANSACTION].split("\n")
        else:
            statement = transaction[TRANSACTION]
            merchant = transaction[TRANSACTION]

        formatted_date = datetime.strptime(f"{date} {year}", "%b %d %Y").strftime(
            "%Y-%m-%d"
        )
        amount = (
            transaction[DEPOSIT].replace(",", "")
            if transaction[DEPOSIT]
            else (
                f"-{transaction[WITHDRAWAL].replace(',', '')}"
                if transaction[WITHDRAWAL]
                else "0.00"
            )
        )

        new_row = {
            "date": formatted_date,
            "merchant": merchant,
            "category": "",
            "account": "",
            "original statement": statement,
            "notes": "",
            "amount": amount,
            "tags": "",
        }
        existing_data.append(new_row)

    # sort all data by date before writing back to the file
    existing_data.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))

    # write sorted data back to CSV
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "date",
            "merchant",
            "category",
            "account",
            "original statement",
            "notes",
            "amount",
            "tags",
        ]
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data)


if __name__ == "__main__":
    main()
