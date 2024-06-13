"""
Reads Scotiabank PDF statements and outputs a CSV file in Monarch format.
"""

from csv import DictWriter
from monarch_transactions import TransactionList
from scotiabank_pdf import ScotiabankPDF

import os


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
        pdf = ScotiabankPDF(path)
        pdf.populate_transaction_coordinates()
        pdf.populate_transactions()
        monarch_raw = monarch_raw + pdf.transactions

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
