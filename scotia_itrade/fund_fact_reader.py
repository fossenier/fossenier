"""
Reads Scotiabank Fund Facts and pulls out the performance data.
"""

from csv import DictWriter
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages
from scotia_fund import Fund

import os

# 1. get all the pdfs
# 2. read each one
# - get the name + series from pg 1
# - get the fund code from pg 1
# - get the yearly performance from pg 2
# - get the MER from pg 3
# 3. store the data to csv
# 4. data analysis
OUTPUT_PATH = "fund_facts.csv"


def main(output_path: str = OUTPUT_PATH, path: str = None) -> None:
    """
    Grabs all PDFs in the current directory and child directories.
    Parses the Scotiabank Fund Fact PDFs.
    Stores the data in a CSV file.
    """
    output_path = "fund_facts.csv"
    target_directory = os.getcwd()

    pdf_paths = []
    # When a specific path is given, only use that one.
    if len(os.sys.argv) > 1:
        pdf_paths = [os.path.join(target_directory, os.sys.argv[1])]
    elif path:
        pdf_paths = [os.path.join(target_directory, path)]
    else:
        # Walk through all directories and subdirectories.
        for dirpath, _, filenames in os.walk(target_directory):
            for filename in filenames:
                # Save Scotiabank Fund Fact PDF paths.
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(dirpath, filename)
                    pdf_paths.append(pdf_path)

    # Extract all fund data from each PDF.
    funds = []
    for path in pdf_paths:
        fund = Fund(path)
        if not fund.invalid:
            funds.append(fund)

    store_funds(output_path, funds)


def store_funds(output_path: str, funds: list[Fund]) -> None:
    """
    Stores the funds in a CSV file.

    args:
        output_path: str - the path to the CSV file
        funds: list[Fund] - the funds to store
    """
    # Find the earliest and latest years.
    earliest_year = None
    latest_year = None
    bad_funds = []
    for fund in funds:
        for year in fund.years:
            try:
                if not earliest_year or year < earliest_year:
                    earliest_year = year
                if not latest_year or year > latest_year:
                    latest_year = year
            except Exception:
                bad_funds.append(fund)
                break
    for bad_fund in bad_funds:
        funds.remove(bad_fund)

    with open(output_path, "w") as file:
        writer = DictWriter(
            file,
            fieldnames=[
                "name",
                "series",
                "code",
                "mer",
                *list(range(earliest_year, latest_year + 1)),
            ],
        )
        # Put header.
        writer.writeheader()
        for fund in funds:
            writer.writerow(
                {
                    "name": fund.name,
                    "series": fund.series,
                    "code": fund.code,
                    "mer": fund.mer,
                    **fund.years,
                }
            )


if __name__ == "__main__":
    main()
