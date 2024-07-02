"""
The object representation of a Scotiabank fund.
"""

from datetime import datetime
from typing import Iterator
from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages
from typing import Dict


x = [1, 2, 3, 4, 5]


class Fund(object):
    def __init__(
        self,
        path: str,
    ) -> None:
        # The file must be a PDF.
        if not path.endswith(".pdf"):
            raise ValueError("The file must be a PDF")
        else:
            self.__path = path

        # Fund historical data.
        self.name = None  # The name of the fund.
        self.code = None  # The distinguisihing code of the fund.
        self.series = None  # The series of the fund.
        self.mer = None  # The (%) management expense ratio of the fund.
        self.years = dict()  # The (%) performance of the fund by year.

        self.__populate_fund_data()

    def __populate_fund_data(self) -> None:
        """
        Opens a PDF file and reads the pages, extracting the data in a manner
        that is hard-coded for Scotiabank Fund Fact files.
        """
        CODE_TOP = 600
        CODE_BOTTOM = 550
        CODE_TOLERANCE = 35
        YEARS_TOP = 663
        YEARS_BOTTOM = 558
        YEARS_LEFT = 340
        YEARS_TOLERANCE = 25
        COLUMN_TOLERANCE = 10
        for page_number, page_layout in enumerate(self.__read_pdf()):
            if page_number == 0:
                for element in page_layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        text = element.get_text().strip()
                        if "1832 Asset Management L.P." in text and not self.name:
                            # Basic LAParams reads in this header as one paragraph.
                            start = text.find("\n")
                            middle = text.find(" - ")

                            self.name = text[start + 1 : middle]

                            raw_series = text[middle + len(" - ") :]
                            self.series = (
                                raw_series.split("/n")[0].replace("Series", "").strip()
                            )
                        elif (
                            abs(element.y1 - CODE_TOP) < CODE_TOLERANCE
                            and abs(element.y0 - CODE_BOTTOM) < CODE_TOLERANCE
                        ):
                            # The fund code is 3 letters and then numbers.
                            try:
                                int(text[3:])
                                self.code = text
                            # This was not the fund code and was just close.
                            except ValueError:
                                pass
                        # The code is found, so stop searching.
                        elif (element.y0 - CODE_TOLERANCE) < CODE_BOTTOM:
                            break
            elif page_number == 1:
                table_elements = dict()
                for element in page_layout:
                    # Data contained within the performance table.
                    if (
                        element.y1 < YEARS_TOP
                        and element.y0 > YEARS_BOTTOM
                        and element.x0 > YEARS_LEFT
                        and isinstance(element, LTTextBoxHorizontal)
                    ):
                        # When finding a new table entry, see if it can be lined up
                        # with an existing column.
                        stored = False
                        for key in table_elements.keys():
                            if abs(key - element.x0) < COLUMN_TOLERANCE:
                                table_elements[key].append(element.get_text().strip())
                                stored = True
                                break

                        if not stored:
                            table_elements[element.x0] = [element.get_text().strip()]

                for pair in table_elements.values():
                    # One item in the stored list is the year, the other the % performance.
                    year, performance = None, None
                    for item in pair:
                        if len(item) == 4 and item.isdigit():
                            year = int(item)
                        else:
                            performance = float(item.replace("%", ""))
                    self.years[year] = performance
            elif page_number == 2:
                for element in page_layout:
                    if isinstance(element, LTTextBoxHorizontal):
                        text = element.get_text().strip()
                        if "of the Fund's expenses were " in text:
                            # This has the start of the MER and the trailing junk.
                            raw_MER = text.split("of the Fund's expenses were ")[1]
                            # This is the pure MER.
                            numerical_MER = raw_MER.split("%")[0]
                            self.mer = float(numerical_MER)

    def __read_pdf(self) -> Iterator[LTPage]:
        """
        Reads a PDF file and returns the pages.
        """
        line_margin = 0.3  # allow multi line textboxes
        char_margin = 1.2  # shrink the default to require words being closer
        laparams = LAParams(char_margin=char_margin, line_margin=line_margin)
        for page_layout in extract_pages(self.__path, laparams=laparams):
            yield page_layout

    def __str__(self) -> str:
        return f"NAME: {self.name} SERIES: {self.series} CODE: {self.code}"
