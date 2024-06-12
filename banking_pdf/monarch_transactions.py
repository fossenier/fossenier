"""
This module contains classes to represent transactions and a list of transactions.
Used for importing banking data to Monarch.
"""

from datetime import datetime
from typing import List
from bisect import bisect_left


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
