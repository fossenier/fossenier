# all necessary imports
from datetime import datetime
from typing import Iterator
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages
from monarch_transactions import Transaction, TransactionList


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
        self.closing_balance = None  # a tuple of the datetime and balance

        self.year = None  # the year of the statement as a str

        self.__date_column = None  # the x0 and x1 of the date column
        self.__deposit_column = None  # the x0 and x1 of the deposit column
        self.__transaction_column = None  # the x0 and x1 of the transaction column
        self.__withdrawal_column = None  # the x0 and x1 of the withdrawal column
        self.__closing_balance_row = None  # the y0 and y1 of the closing balance row

        # the y0 and y1 of the transaction rows mapped to a transaction
        self.__transaction_rows = dict()

    def populate_closing_balance(self) -> None:
        """
        Populates the closing balance of the PDF statement.
        """
        # vertical tolerance
        BALANCE_TOLERANCE = 5
        if not self.__closing_balance_row:
            # the PDF does not have the necessary columns
            print(f"Empty PDF at {self.__path}")
            return

        for i, page_layout in enumerate(self.read_pages(self.__path)):
            if i > 0:
                break
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    if (
                        abs(self.__closing_balance_row[0] - element.y0)
                        < BALANCE_TOLERANCE
                        and abs(self.__closing_balance_row[1] - element.y1)
                        < BALANCE_TOLERANCE
                        and len(text) < 15  # allows up to one billion dollars
                    ):
                        # prepare the text to become a float
                        text = text.replace(",", "")
                        text = text.replace("$", "")

                        latest_date = datetime.strptime(f"Jan 1 1900", "%b %d %Y")
                        # find the latest date of the month (closing day)
                        for _, transaction in self.__transaction_rows.items():
                            if transaction.date > latest_date:
                                latest_date = transaction.date

                        # Do not allow undated pdfs
                        if latest_date == datetime.strptime(f"Jan 1 1900", "%b %d %Y"):
                            self.closing_balance = (None, None)
                        else:
                            self.closing_balance = (latest_date, float(text))
                            break

    def populate_transaction_coordinates(self) -> None:
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

                    # find row useful for monthly balance
                    elif text.startswith("Closing Balance on "):
                        self.__closing_balance_row = (element.y0, element.y1)

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

    def populate_transactions(self) -> None:
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
