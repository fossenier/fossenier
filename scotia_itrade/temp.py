



            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    # Read name, series, and fund code from the first page.
                    if page_number == 0:
                        if "1832 Asset Management L.P." in text:
                            # Basic LAParams reads in this header as one paragraph of two lines.
                            full_name = text.split("\n")[1]
                            # The name and series are separated by " - ".
                            self.name, full_series = full_name.split(" - ")
                            # Remove "Series" from the series.
                            self.series = full_series.replace("Series", "").strip()
                        elif (abs(element.y1 - CODE_TOP) < CODE_TOLERANCE
                            and abs(element.y0 - CODE_BOTTOM) < CODE_TOLERANCE
                            and len(text) == 6):
                            # The fund code is 3 letters and 3 numbers.
                            try:
                                int(text[3:])
                                self.code = text
                            # This was not the fund code and was just some 6 letter word.
                            except ValueError:
                                pass
                    if page_number == 1:
                        if "Management Expense Ratio" in text:
                            # The MER is the next line.
                            self.MER = float(text.split("\n")[1].replace("%", ""))