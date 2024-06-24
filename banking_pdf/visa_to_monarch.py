"""
Takes a Scotia Visa transactions .csv and outputs a Monarch transactions .csv
"""

from csv import DictWriter, DictReader
from monarch_transactions import Transaction, TransactionList
from scotiabank_pdf import ScotiabankPDF

import os
import sys


def main() -> None:
    """
    Reads one Scotia Visa transactions CSV file.
    Outputs to a Monarch CSV file, without the account name. (Put that in yourself.)
    """
    # treat the first cla as the path
    if len(os.sys.argv) > 1:
        path = os.sys.argv[1]
    else:
        print("Please provide a path to a Scotia Visa transactions CSV file.")
        sys.exit(1)

    # WARNING no touchy: my .gitignore is set to ignore this file
    output_path = "private.csv"

    # get the current directory
    target_directory = os.getcwd()
    path = os.path.join(target_directory, path)

    # create the output CSV
    with open(output_path, "w") as file:
        # put the right columns for the Monarch format
        file.write(
            "Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags\n"
        )

    # extract transactions from the CSV
    transactions = read_transactions(path)

    store_transactions(output_path, transactions)


def read_transactions(file_path: str) -> TransactionList:
    """
    Reads transactions from a Scotia Visa CSV file and outputs to a Monarch CSV file.
    Filter,Date,Description,Status,Type of Transaction,Amount

    args:
        file_path: str - the path to the Scotia Visa CSV file

    rtype:
        TransactionList - the transactions read from the Scotia Visa CSV file
    """
    transactions = TransactionList()

    with open(file_path, "r") as file:
        reader = DictReader(file)
        for row in reader:
            date = row["Date"]
            merchant = row["Description"]
            category = ""
            account = ""
            original_statement = row["Description"]
            notes = ""
            amount = float(row["Amount"])
            tags = ""

            if row["Type of Transaction"] == "Debit":
                amount = -amount

            transactions.add_transaction(
                Transaction(
                    date,
                    merchant,
                    category,
                    account,
                    original_statement,
                    notes,
                    amount,
                    tags,
                )
            )

    return transactions


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
                    "Date",
                    "Merchant",
                    "Category",
                    "Account",
                    "Original Statement",
                    "Notes",
                    "Amount",
                    "Tags",
                ],
            )

            # formatting
            writer.writerow(
                {
                    "Date": transaction.date,
                    "Merchant": transaction.merchant,
                    "Category": transaction.category,
                    "Account": transaction.account,
                    "Original Statement": transaction.original_statement,
                    "Notes": transaction.notes,
                    "Amount": transaction.amount,
                    "Tags": transaction.tags,
                }
            )


if __name__ == "__main__":
    main()
