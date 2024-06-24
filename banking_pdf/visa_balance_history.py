"""
Use a csv of the Monarch format and my banking PDFs to recreate my balance history over time.
"""

from csv import DictWriter, DictReader
from datetime import datetime, timedelta
from monarch_transactions import TransactionList
from scotiabank_pdf import ScotiabankPDF
from typing import List, Tuple

import os
import sys


def main() -> None:
    """
    Reads in a Monarch transactions CSV file and outputs a Monarch balance history CSV file.
    """
    if len(sys.argv) <= 1:
        print("Please provide a Monarch CSV file path")
        sys.exit(1)
    path = sys.argv[1]

    output_path = "private.csv"

    target_directory = os.getcwd()
    path = os.path.join(target_directory, path)

    transactions = read_transactions(path)

    # Initialize balance and dates
    start_date = transactions[0][0]
    end_date = transactions[-1][0]
    balance = 0.0

    # Generate daily balances
    daily_balances = generate_daily_balances(
        transactions, start_date, end_date, balance
    )

    # Store balances to CSV
    store_balances(output_path, daily_balances)


def generate_daily_balances(
    transactions: List[Tuple[datetime, float]],
    start_date: datetime,
    end_date: datetime,
    initial_balance: float,
) -> List[Tuple[datetime, float]]:
    """
    Generates daily balances from transactions.
    """
    daily_balances = []
    balance = initial_balance
    transaction_index = 0

    current_date = start_date

    while current_date <= end_date:
        while (
            transaction_index < len(transactions)
            and transactions[transaction_index][0] == current_date
        ):
            balance += transactions[transaction_index][1]
            transaction_index += 1

        daily_balances.append((current_date, balance))
        current_date += timedelta(days=1)

    return daily_balances


def store_balances(
    output_path: str, daily_balances: List[Tuple[datetime, float]]
) -> None:
    """
    Stores the daily balances in a CSV file.
    """
    with open(output_path, "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["Date", "Balance", "Account"])
        writer.writeheader()

        for date, balance in daily_balances:
            writer.writerow(
                {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Balance": balance,
                    "Account": "Scotiabank",
                }
            )


def read_transactions(file_path: str) -> List[Tuple[datetime, float]]:
    """
    Reads a Monarch transactions CSV file and returns a list of (datetime, amount) tuples.
    """
    transactions = []
    with open(file_path, "r") as file:
        reader = DictReader(file)
        for row in reader:
            date = datetime.strptime(row["Date"], "%Y-%m-%d")
            amount = float(row["Amount"])
            transactions.append((date, amount))

    # Sort transactions by date
    transactions.sort(key=lambda x: x[0])
    return transactions


def store_transactions(file_path: str, transactions: TransactionList) -> None:
    """
    Stores the transactions in a CSV file by appending them in chronological order.
    """
    with open(file_path, "a", newline="") as file:
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
        writer.writeheader()

        for transaction in transactions.transactions():
            if "\n" in transaction.original_statement:
                separated = transaction.original_statement.split("\n")
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
