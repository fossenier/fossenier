"""
Reads Scotiabank Fund Facts and pulls out the performance data.
"""

from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages
from scotia_fund import Fund

# 1. get all the pdfs
# 2. read each one
# - get the name + series from pg 1
# - get the fund code from pg 1
# - get the yearly performance from pg 2
# - get the MER from pg 3
# 3. store the data to csv
# 4. data analysis

def main():
    pass

if __name__ == "__main__":
    main()

