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
        self.invalid = False  # The fund is invalid and should not be stored.

        self.__populate_fund_data()

    def __populate_fund_data(self) -> None:
        """
        Opens a PDF file and reads the pages, extracting the data in a manner
        that is hard-coded for Scotiabank Fund Fact files.
        """
        CODE_TOP = 600
        CODE_BOTTOM = 550
        CODE_TOLERANCE = 35
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
                        # Ignore the fund if you need a million dollars to invest.
                        elif "$1,000,000 initial" in text:
                            self.invalid = True
                        else:
                            # The fund code is 3 letters and then numbers.
                            try:
                                words = text.split(" ")
                                possible_code = words[0]
                                # This is another part of the document.
                                if "$" in possible_code or "1832" in possible_code:
                                    raise ValueError
                                numerical_code = int(possible_code[3:])
                                # This is random text.
                                if numerical_code < 100:
                                    raise ValueError
                                self.code = possible_code
                            # This was not the fund code and was just close.
                            except ValueError:
                                pass
            elif page_number == 1:
                cached_elements = []
                table_y1 = None  # The top of the performance graph (taken as the top of the highest % symbol).
                table_y0 = None  # The bottom of the performance graph (taken as the top of the following header).
                table_x0 = None  # The left of the performance graph (taken as the x1 of the rightmost % symbol).
                caching = True
                for element in page_layout:
                    cached_elements.append(element)
                    if caching and isinstance(element, LTTextBoxHorizontal):
                        text = element.get_text().strip()
                        if "Best and worst 3-month returns" in text:
                            table_y0 = element.y1
                            # Assume no more table data
                            caching = False
                        # Not a year or performance indicator.
                        if len(text) > 5:
                            continue
                        elif "%" in text:
                            if not table_y1 or element.y1 > table_y1:
                                table_y1 = element.y1
                            if not table_x0 or element.x1 > table_x0:
                                table_x0 = element.x1
                    elif not caching and isinstance(element, LTTextBoxHorizontal):
                        text = element.get_text().strip()
                        if "of the Fund's expenses were " in text:
                            # This has the start of the MER and the trailing junk.
                            raw_MER = text.split("of the Fund's expenses were ")[1]
                            # This is the pure MER.
                            numerical_MER = raw_MER.split("%")[0]
                            self.mer = float(numerical_MER)

                # The performance table was not found (i.e. has not matured to one year).
                if not table_y1 or not table_y0 or not table_x0:
                    self.invalid = True
                    break

                # Parse the performance table.
                table_elements = dict()
                for element in cached_elements:
                    # Data contained within the performance table.
                    if (
                        element.y1 < table_y1
                        and element.y0 > table_y0
                        and element.x0 > table_x0
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
