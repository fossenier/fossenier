"""
Reads Scotiabank PDF statements and outputs a CSV file in Monarch format.
"""

from bisect import bisect_left
from csv import DictWriter
from datetime import datetime
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from typing import Iterator, List

import os


class Transaction:
    """
    Represents a transaction to be imported into Monarch.
    """

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

    def __lt__(self, other):
        return self.date < other.date


class TransactionList:
    """
    Represents a set of transactions in the Monarch. For example, from a bank's
    monthly statement.
    """

    def __init__(self, transactions: List[Transaction] = None) -> None:
        # maintain a sorted list of transactions
        self.__transactions = []

        if transactions:
            # there is one transaction to add
            if isinstance(transactions, Transaction):
                self.add_transaction(transactions)
            # there are multiple transactions to add
            else:
                for transaction in transactions:
                    self.add_transaction(transaction)

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Adds a transaction to the list of transactions, maintaining the order.
        """
        # insert the transaction in the correct order, using a quick and efficient search
        index = bisect_left(self.__transactions, transaction)
        self.__transactions.insert(index, transaction)

    def __add__(self, other):
        # ChatGPT wrote this method
        """
        Merges two TransactionList instances.
        """
        if not isinstance(other, TransactionList):
            raise ValueError("Can only add TransactionList to TransactionList")

        merged_transactions = []
        i, j = 0, 0
        while i < len(self.__transactions) and j < len(other.__transactions):
            if self.__transactions[i] < other.__transactions[j]:
                merged_transactions.append(self.__transactions[i])
                i += 1
            else:
                merged_transactions.append(other.__transactions[j])
                j += 1

        # append remaining transactions from either list
        while i < len(self.__transactions):
            merged_transactions.append(self.__transactions[i])
            i += 1

        while j < len(other.__transactions):
            merged_transactions.append(other.__transactions[j])
            j += 1

        return TransactionList(merged_transactions)

    def transactions(self) -> List[Transaction]:
        """
        NOTE: Do not modify the transactions directly. Use add_transaction() instead.
        """
        return self.__transactions


class ScotiabankPDF(object):
    """
    Represents a Scotiabank PDF monthly statement.
    """

    def __init__(self, path: str) -> None:
        if not path.endswith(".pdf"):
            raise ValueError("The file must be a PDF")
        else:
            self.__path = path

        self.transactions = TransactionList()

        self.year = None  # the year of the statement as a str

        self.__date_column = None  # the x0 and x1 of the date column
        self.__deposit_column = None  # the x0 and x1 of the deposit column
        self.__transaction_column = None  # the x0 and x1 of the transaction column
        self.__withdrawal_column = None  # the x0 and x1 of the withdrawal column

        # the y0 and y1 of the transaction rows mapped to a transaction
        self.__transaction_rows = dict()
        self.__populate_coordinates()
        self.__populate_transactions()

    def __populate_coordinates(self) -> None:
        """
        Populates the transaction coordinates of the PDF statement.
        """
        # horizontal tolerance
        DATE_X0 = 1
        DATE_X1 = 20

        for i, page_layout in enumerate(self.read_pages(self.__path)):
            for element in page_layout:
                # save coordinates for columns and rows
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()

                    # grab the year from near the top of the document
                    if not self.year and text.startswith("Opening Balance on "):
                        raw_time = text.split(" ")
                        self.year = raw_time[5]

                    # find all columns useful for transactions
                    elif text == "Date":
                        self.__date_column = (element.x0, element.x1)
                    elif text == "Transactions":
                        self.__transaction_column = (element.x0, element.x1)
                    elif text == "Amounts\nwithdrawn ($)":
                        self.__withdrawal_column = (element.x0, element.x1)
                    elif text == "Amounts\ndeposited ($)":
                        self.__deposit_column = (element.x0, element.x1)

                    # find all rows of transactions
                    # NOTE transactions appear below the date column header
                    elif (
                        self.__date_column
                        and abs(self.__date_column[0] - element.x0) < DATE_X0
                        and abs(self.__date_column[1] - element.x1) < DATE_X1
                    ):
                        if len(text) > 6:
                            text = text[-5:]
                        date = datetime.strptime(f"{text} {self.year}", "%b %d %Y")
                        self.__transaction_rows[(i, element.y0, element.y1)] = (
                            Transaction(date=date)
                        )

    def __populate_transactions(self) -> None:
        """
        Populates the transactions based on the populated coordinate data for the PDF.
        """
        if (
            not self.__date_column
            or not self.__deposit_column
            or not self.__transaction_column
            or not self.__withdrawal_column
            or not self.__transaction_rows
        ):
            # the PDF does not have the necessary columns
            print(f"Empty PDF at {self.__path}")
            return

        def get_transaction(page: int, y0: float, y1: float) -> Transaction:
            """
            Checks the y0 and y1 in self.transaction_rows for a transaction.
            """
            # vertical tolerances
            ROW_Y0 = 15
            ROW_Y1 = 100
            for (i, row_y0, row_y1), transaction in self.__transaction_rows.items():
                if (
                    abs(row_y0 - y0) < ROW_Y0
                    and abs(row_y1 - y1) < ROW_Y1
                    and i == page
                ):
                    return transaction

        TRANSACTION_X0 = 1
        TRANSACTION_X1 = 220
        AMOUNT_X0 = 50
        AMOUNT_X1 = 5
        for i, page_layout in enumerate(self.read_pages(self.__path)):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()

                    # save the original statement
                    if (
                        abs(self.__transaction_column[0] - element.x0) < TRANSACTION_X0
                        and abs(self.__transaction_column[1] - element.x1)
                        < TRANSACTION_X1
                    ):
                        transaction = get_transaction(i, element.y0, element.y1)
                        if transaction:
                            transaction.original_statement = text

                    # populate the transaction amount
                    elif (
                        abs(self.__deposit_column[0] - element.x0) < AMOUNT_X0
                        and abs(self.__deposit_column[1] - element.x1) < AMOUNT_X1
                    ):
                        transaction = get_transaction(i, element.y0, element.y1)
                        if transaction:
                            transaction.amount = text.replace(",", "")
                    elif (
                        abs(self.__withdrawal_column[0] - element.x0) < AMOUNT_X0
                        and abs(self.__withdrawal_column[1] - element.x1) < AMOUNT_X1
                    ):
                        transaction = get_transaction(i, element.y0, element.y1)
                        if transaction:
                            transaction.amount = "-" + text.replace(",", "")

        for _, transaction in self.__transaction_rows.items():
            # skip opening and closing balance
            if transaction.original_statement in ["Opening Balance", "Closing Balance"]:
                continue
            self.transactions.add_transaction(transaction)

    def read_pages(self, path: str) -> Iterator[LTPage]:
        """
        Reads the PDF file with LAParams tailored for Scotiabank PDFs.
        Allows multi line and forces sentences to require text closer together.

        args:
            path: str - the path to the PDF file

        rtype:
            Iterator[LTPage] - the pages of the PDF
        """
        line_margin = 0.3  # allow multi line textboxes
        char_margin = 1.2  # shrink the default to require words being closer
        laparams = LAParams(char_margin=char_margin, line_margin=line_margin)

        for page_layout in extract_pages(path, laparams=laparams):
            yield page_layout


def main(path: str = None) -> None:
    """
    Reads all (or just one) Scotiabank PDF statements in the current directory and child directories.
    Outputs to a Monarch CSV file, without the account name. (Put that in yourself.)
    """
    # check for command line args, and pull the first one and treat as path
    if len(os.sys.argv) > 1:
        path = os.sys.argv[1]

    # WARNING no touchy: my .gitignore is set to ignore this file
    output_path = "private.csv"

    # get the current directory
    target_directory = os.getcwd()

    # create the output CSV
    with open(output_path, "w") as file:
        # put the right columns for the Monarch format
        file.write(
            "date,merchant,category,account,original statement,notes,amount,tags\n"
        )

    pdf_paths = []
    # when a specific path is given, only use that one
    if path:
        pdf_paths = [os.path.join(target_directory, path)]
    else:
        # walk through all directories and subdirectories
        for dirpath, _, filenames in os.walk(target_directory):
            for filename in filenames:
                # save Scotiabank PDF paths
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(dirpath, filename)
                    pdf_paths.append(pdf_path)

    # extract all transactions from each PDF
    monarch_raw = TransactionList()
    for path in pdf_paths:
        monarch_raw = monarch_raw + ScotiabankPDF(path).transactions

    store_transactions(output_path, monarch_raw)


def store_transactions(file_path: str, transactions: TransactionList) -> None:
    """
    Stores the transactions in a CSV file by appending them in chronological order.

    args:
        file_path: str - the path to the CSV file
        transactions: TransactionList - the transactions to store
    """
    for transaction in transactions.transactions():
        with open(file_path, "a") as file:
            writer = DictWriter(
                file,
                fieldnames=[
                    "date",
                    "merchant",
                    "category",
                    "account",
                    "original statement",
                    "notes",
                    "amount",
                    "tags",
                ],
            )

            # formatting
            if "\n" in transaction.original_statement:
                separated = transaction.original_statement.split("\n")
                # the cost was tucked into the merchant name
                # TODO this is a hacky solution, but it works for now
                # 1 PDF in 7 years tripped needed this
                if len(separated) > 2:
                    print(f"WARNING: {separated}")
                    separated.pop(1)
                statement, merchant = separated
            else:
                statement = transaction.original_statement
                merchant = transaction.original_statement

            formatted_date = transaction.date.strftime("%Y-%m-%d")

            writer.writerow(
                {
                    "date": formatted_date,
                    "merchant": merchant,
                    "category": transaction.category,
                    "account": transaction.account,
                    "original statement": statement,
                    "notes": transaction.notes,
                    "amount": transaction.amount,
                    "tags": transaction.tags,
                }
            )


if __name__ == "__main__":
    main()
