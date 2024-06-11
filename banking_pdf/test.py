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

    def __populate_transactions(self) -> None:
        """
        Populates the location data of the PDF statement.

        args:
            path: str - the path to the PDF file
        """

        def get_transaction(y0: float, y1: float) -> Transaction:
            """
            Checks the y0 and y1 in self.transaction_rows for a transaction.
            """
            ROW_Y0 = 10
            ROW_Y1 = 100
            for (row_y0, row_y1), transaction in self.__transaction_rows.items():
                if abs(row_y0 - y0) < ROW_Y0 and abs(row_y1 - y1) < ROW_Y1:
                    return transaction

        DATE_X0 = 1
        DATE_X1 = 20
        TRANSACTION_X0 = 1
        TRANSACTION_X1 = 180
        AMOUNT_X0 = 50
        AMOUNT_X1 = 5
        for page_layout in self.__pages:
            for element in page_layout:
                # save coordinates for the desired columns
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    # if len(text) >= 6:
                    #     print(text, "\n")

                    # grab the year from near the top of the document
                    if not self.year and text.startswith("Opening Balance on "):
                        raw_time = text.split(" ")
                        self.year = raw_time[5]

                
                    elif (
                        self.__withdrawal_column
                        and abs(self.__withdrawal_column[0] - element.x0) < AMOUNT_X0
                        and abs(self.__withdrawal_column[1] - element.x1) < AMOUNT_X1
                    
                    ):
                        transaction = get_transaction(element.y0, element.y1)
                        if transaction:
                            transaction.amount = f"-{text.replace(",", "")}"

                    # all other data is not needed
                    else:
                        continue
        for _, transaction in self.__transaction_rows.items():
            # skip opening and closing balance
            if transaction.original_statement in ["Opening Balance", "Closing Balance"]:
                continue
            self.transactions.add_transaction(transaction)
