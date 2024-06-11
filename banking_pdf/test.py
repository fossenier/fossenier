from bisect import bisect_left
from csv import DictReader, DictWriter
from datetime import datetime
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from typing import Dict, Iterator, List, Tuple

import os

class Transaction(object):
    def __init__(
        self,
        date: datetime = datetime.now(),
        merchant: str = "",
        category: str = "",
        account: str = "",
        original_statement: str = "",
        notes: str = "",
        amount: str = "0.00",
        tags: str = "",
    ) -> None:
        self.date = date
        self.merchant = merchant
        self.category = category
        self.account = account
        self.original_statement = original_statement
        self.notes = notes
        self.amount = amount
        self.tags = tags

def populate_location_data(self) -> None:
    """
    Populates the location data of the PDF statement.

    args:
        path: str - the path to the PDF file
    """

    def get_transaction(y0: float, y1: float) -> Transaction:
        """
        Checks the y0 and y1 in self.transaction_rows for a transaction.
        """
        ROW_Y0 = 0.5
        ROW_Y1 = 50
        for (row_y0, row_y1), transaction in self.transaction_rows.items():
            if row_y0 - ROW_Y0 < y0 and row_y1 + ROW_Y1 > y1:
                return transaction

    DATE_X0 = 1
    DATE_X1 = 20
    TRANSACTION_X0 = 1
    TRANSACTION_X1 = 180
    for page_layout in self.pages:
        for element in page_layout:
            # save coordinates for the desired columns
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()

                # grab the year from near the top of the document
                if not self.year and text.startswith("Opening Balance on "):
                    raw_time = text.split(" ")
                    self.year = raw_time[5]

                # find all columns useful for transactions
                elif text == "Date":
                    self.date_column = (element.x0, element.x1)
                elif text == "Transactions":
                    self.transaction_column = (element.x0, element.x1)
                elif text == "Amounts\nwithdrawn ($)":
                    self.withdrawal_column = (element.x0, element.x1)
                elif text == "Amounts\ndeposited ($)":
                    self.deposit_column = (element.x0, element.x1)

                # find all rows of transactions
                # NOTE transactions appear below the date column header
                elif (
                    self.date_column
                    and self.date_column[0] - DATE_X0 < element.x0
                    and self.date_column[1] + DATE_X1 > element.x1
                ):
                    print(text)
                    date = datetime.strptime(f"{text} {self.year}", "%b %d %Y")
                    self.transaction_rows[(element.y0, element.y1)] = Transaction(
                        date=date
                    )

                # populate the transaction original statement
                elif (
                    self.transaction_column
                    and self.transaction_column[0] - TRANSACTION_X0 < element.x0
                    and self.transaction_column[1] + TRANSACTION_X1 > element.x1
                
                ):
                    # print(text)
                    transaction = get_transaction(element.y0, element.y1)
                    if transaction:
                        transaction.original_statement = text
                
                # populate the transaction amount
                elif (
                    self.deposit_column
                    and self.deposit_column[0] - TRANSACTION_X0 < element.x0
                    and self.deposit_column[1] + TRANSACTION_X1 > element.x1
                ):
                    transaction = get_transaction(element.y0, element.y1)
                    if transaction:
                        transaction.amount = text.replace(",", "")
                elif (
                    self.withdrawal_column
                    and self.withdrawal_column[0] - TRANSACTION_X0 < element.x0
                    and self.withdrawal_column[1] + TRANSACTION_X1 > element.x1
                ):
                    transaction = get_transaction(element.y0, element.y1)
                    if transaction:
                        transaction.amount = f"-{text.replace(",", "")}"
                        
                # all other data is not needed
                else:
                    pass
