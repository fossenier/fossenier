"""
The object representation of a Scotiabank fund.
"""
from datetime import datetime
from typing import Iterator
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages
from typing import Dict


class Fund(object):
    def __init__(
        self,
        path: str,
    ) -> None:
        self.name = None  # the name of the fund
        self.code = None  # the distinguisihing code of the fund
        self.series = None  # the series of the fund
        self.MER = None  # the (%) management expense ratio of the fund
        self.years = None  # the (%) performance of the fund by year
