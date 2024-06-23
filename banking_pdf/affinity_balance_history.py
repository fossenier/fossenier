"""
Use a csv of the Monarch format and my banking PDFs to recreate my balance history over time.
"""

from csv import DictWriter
from datetime import datetime, timedelta
from monarch_transactions import TransactionList
from affinity_pdf import AffinityPDF
from typing import List, Tuple

import os


def main(path: str = None, balance: float = None) -> None:
    """
    Reads all (or just one) Affinity PDF statements in the current directory and child directories.
    Outputs to a Monarch CSV file for account balance history.
    """
    # check for command line args, and pull the first one and treat as balance, the second as path
    if len(os.sys.argv) > 1:
        balance = float(os.sys.argv[1])
    if len(os.sys.argv) > 2:
        path = os.sys.argv[2]

    # WARNING no touchy: my .gitignore is set to ignore this file
    output_path = "private.csv"
    transactions_path = "/Users/admin/Downloads/affinityTransactions/transactions.csv"

    # get the current directory
    target_directory = os.getcwd()

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

    # extract all guaranteed balances from each PDF
    guaranteed_balances = []
    for path in pdf_paths:
        pdf = AffinityPDF(path)
        pdf.populate_transaction_coordinates()
        pdf.populate_closing_balance()
        if pdf.closing_balance[0]:
            guaranteed_balances.append(pdf.closing_balance)

    store_balances(output_path, transactions_path, balance, guaranteed_balances)


def store_balances(
    output_path: str,
    transactions_path: str,
    balance: float,
    monthly_balances: List[Tuple[datetime, float]],
) -> None:
    """
    Takes in a Monarch transactions csv, a starting balance, and a list of guaranteed balances.
    Goes back in time creating a daily balance history.
    """
    with open(output_path, "w") as file:
        # put the file header
        writer = DictWriter(file, fieldnames=["Date", "Balance", "Account"])
        writer.writeheader()

        # transactions and balances to iterate through
        transactions = read_transactions(transactions_path)
        balances = sorted(monthly_balances, key=lambda x: x[0])

        # the next transaction and balance
        next_transaction = transactions.pop()
        next_balance = balances.pop()

        current_date = datetime.now()
        while True:
            # step to yesterday
            current_date -= timedelta(days=1)

            # if there are no more transactions or balances, break
            if not next_transaction and not next_balance:
                break

            # when there is a balance for today, update the balance
            while next_balance and next_balance[0].date() == current_date.date():
                balance = next_balance[1]
                try:
                    next_balance = balances.pop()
                except IndexError:
                    next_balance = None

            # when there are transactions for today, update the balance
            while (
                next_transaction and next_transaction[0].date() == current_date.date()
            ):
                balance -= next_transaction[1]
                try:
                    next_transaction = transactions.pop()
                except IndexError:
                    next_transaction = None

            # write the balance for today
            writer.writerow(
                {
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Balance": balance,
                    "Account": "Scotiabank",
                }
            )


def read_transactions(file_path: str) -> List[Tuple[datetime, float]]:
    """
    Reads a Monarch transactions CSV file and returns an iterator of datetime and balance tuples.
    Most recent date to most ancient date.

    args:
        file_path: str - the path to the CSV file
    """
    with open(file_path, "r") as file:
        # skip the header
        next(file)

        lines = [line.strip().split(",") for line in file]
        return [
            (datetime.strptime(line[0], "%Y-%m-%d"), float(line[6].replace("$", "")))
            for line in lines
        ]


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
